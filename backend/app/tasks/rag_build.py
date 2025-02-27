import traceback
from uuid import UUID
from sqlmodel import Session, select
from celery.utils.log import get_task_logger
from llama_index.llms.openai import OpenAI
from llama_index.llms.gemini import Gemini

from app.celery import app as celery_app
from app.core.db import engine
from app.models import (
    Document as DBDocument,
    Chunk as DBChunk,
    DocIndexTaskStatus,
    KgIndexStatus,
)
from app.rag.build import BuildService
from app.rag.types import OpenAIModel, GeminiModel
from app.utils.dspy import get_dspy_lm_by_llama_llm


logger = get_task_logger(__name__)


@celery_app.task
def build_vector_index_from_document(document_id: int):
    with Session(engine) as session:
        db_document = session.get(DBDocument, document_id)
        if db_document is None:
            logger.error(f"Document {document_id} not found")
            return

        if db_document.index_status != DocIndexTaskStatus.PENDING:
            logger.info(f"Document {document_id} not in pending state")
            return

        db_document.index_status = DocIndexTaskStatus.RUNNING
        session.commit()

        if (
            session.exec(
                select(DBChunk).where(DBChunk.document_id == document_id)
            ).first()
            is not None
        ):
            logger.info(f"Document {document_id} already indexed")
            return

        try:
            # TODO: user should be able to choose the chat engine
            llm = Gemini(model=GeminiModel.GEMINI_15_FLASH)
            # llm = OpenAI(model=OpenAIModel.GPT_35_TURBO)
            build_service = BuildService(
                llm=llm,
                dspy_lm=get_dspy_lm_by_llama_llm(llm),
            )

            build_service.build_vector_index_from_document(session, db_document)
        except Exception:
            error_msg = traceback.format_exc()
            logger.error(f"Error while indexing document {document_id}: {error_msg}")
            db_document.index_status = DocIndexTaskStatus.FAILED
            db_document.index_result = error_msg
            session.commit()
            return

        db_document.index_status = DocIndexTaskStatus.COMPLETED
        session.commit()
        logger.info(f"Document {document_id} indexed successfully")


@celery_app.task
def build_kg_index_from_chunk(chunk_id: UUID):
    with Session(engine) as session:
        db_chunk = session.get(DBChunk, chunk_id)
        if db_chunk is None:
            logger.error(f"Chunk {chunk_id} not found")
            return

        if db_chunk.index_status != KgIndexStatus.PENDING:
            logger.info(f"Chunk {chunk_id} not in pending state")
            return

        db_chunk.index_status = KgIndexStatus.RUNNING
        session.commit()

        try:
            llm = Gemini(model=GeminiModel.GEMINI_15_FLASH)
            build_service = BuildService(
                llm=llm,
                dspy_lm=get_dspy_lm_by_llama_llm(llm),
            )
            build_service.build_kg_index_from_chunk(session, db_chunk)
        except Exception:
            error_msg = traceback.format_exc()
            logger.error(f"Error while indexing chunk {chunk_id}: {error_msg}")
            db_chunk.index_status = KgIndexStatus.FAILED
            db_chunk.index_result = error_msg
            session.commit()
            return

        db_chunk.index_status = KgIndexStatus.COMPLETED
        session.commit()
        logger.info(f"Chunk {chunk_id} indexed successfully")

import { getChatEngine } from '@/api/chat-engines';
import { AdminPageHeading } from '@/components/admin-page-heading';
import { ChatEngineDetails } from '@/components/chat-engine/chat-engine-details';
import { Card, CardContent, CardTitle } from '@/components/ui/card';
import { requireAuth } from '@/lib/auth';

export default async function ChatEnginePage ({ params }: { params: { id: string } }) {
  await requireAuth();

  const chatEngine = await getChatEngine(parseInt(params.id));

  return (
    <>
      <AdminPageHeading title={`Chat Engine - ${chatEngine.name}`} />
      <div className="xl:pr-side max-w-screen-lg">
        <Card>
          <CardContent className='pt-4'>
            <ChatEngineDetails chatEngine={chatEngine} />
          </CardContent>
        </Card>
      </div>
    </>
  );
}

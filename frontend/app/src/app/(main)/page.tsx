'use client';

import { Ask } from '@/components/chat/ask';
import { useAsk } from '@/components/chat/use-ask';
import { withReCaptcha } from '@/components/security-setting-provider';
import { Button } from '@/components/ui/button';
import { useSettingContext } from '@/components/website-setting-provider';
import NextLink from 'next/link';

export default function Page () {
  const { loading, setEngine, ask, engine } = useAsk();
  const { website: { homepage }, security } = useSettingContext();

  return (
    <div className="h-screen">
      <div className="lg:h-[calc(100%-var(--ask-referral-height))] h-2/3 p-4 lg:p-0 flex flex-col items-center justify-center gap-4 relative">
        <h1 className="text-2xl sm:text-4xl font-light text-center">
          {homepage?.title || ''}
        </h1>
        <p className="font-light dark:text-gray-300 text-gray-500 mb-4 w-4/5 md:w-auto text-center">
          {homepage?.description || ''}
        </p>
        <Ask className="px-4 w-full lg:w-2/3" loading={loading} ask={ask} engine={engine} setEngine={setEngine} />
        {homepage?.example_questions && (<ul className="flex gap-2 flex-wrap px-4 w-full lg:w-2/3">
          {homepage.example_questions.map(item => (
            <li key={item.text}>
              <Button
                className="g-recaptcha font-normal text-xs"
                disabled={loading}
                variant="secondary"
                size="sm"
                onClick={() => {
                  withReCaptcha({
                    action: 'ask',
                    siteKey: security?.google_recaptcha_site_key || '',
                    mode: security?.google_recaptcha,
                  }, ({ token, action }) => {
                    ask(item.text, {
                      headers: {
                        'X-Recaptcha-Token': token,
                        'X-Recaptcha-Action': action,
                      },
                    });
                  });
                }}
              >
                {item.text}
              </Button>
            </li>
          ))}
        </ul>)}
      </div>
      <div className="lg:h-[var(--ask-referral-height)] h-1/3 flex lg:justify-center justify-end items-center gap-4 lg:flex-row flex-col pb-4 lg:pb-0" style={{ display: 'auto' }}>
        {homepage?.footer_links?.map(link => (
          <NextLink key={link.text} href={link.href} target="_blank" className="font-light text-sm hover:underline opacity-50 flex justify-center">
            {link.text}
          </NextLink>
        ))}
      </div>
    </div>
  );
}

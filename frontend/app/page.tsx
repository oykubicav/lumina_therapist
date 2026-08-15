"use client";

import { useEffect, useState } from "react";
import { hasConsent } from "@/lib/consent";
import ConsentModal from "@/components/ConsentModal";
import ChatWindow from "@/components/ChatWindow";
import Landing from "@/components/Landing";
import { hasDecided, shouldPromptNow } from "@/lib/assessments";
import AssessmentOptInModal from "@/components/AssessmentOptInModal";


/**
 * Page state machine:
 *   "landing" — user hasn't started yet, show hero
 *   "consent" — user clicked "Sohbete başla" but consent not yet given
 *   "chat"    — consent given, show chat
 * On mount: if consent already granted (returning user), skip landing.
 */
export default function Page() {
  const [state, setState] = useState<"landing" | "consent" | "chat">("landing");
  const [mounted, setMounted] = useState(false);
  const [showOptIn, setShowOptIn] = useState(false);


  useEffect(() => {
    setMounted(true);
    // Returning visitor with prior consent → skip landing
    if (hasConsent()) {
      setState("chat");
    }
  }, []);

  useEffect(() => {
    if (state === "chat" && !hasDecided()) {
      // Küçük bir gecikme — chat açılsın, sonra modal gelsin, uçuşmuş hissi vermesin
      const timer = setTimeout(() => setShowOptIn(true), 2500);
      return () => clearTimeout(timer);
    }
  }, [state]);

  if (!mounted) {
    // SSR pass — render an empty shell to avoid hydration mismatch
    return null;
  }

  if (state === "chat") {
    return (
      <>
        <ChatWindow />
        {showOptIn && <AssessmentOptInModal onDismiss={() => setShowOptIn(false)} />}
      </>
    );
  }

  return (
    <>
      <Landing onStart={() => setState("consent")} />
      {state === "consent" && (
        <ConsentModal onGranted={() => setState("chat")} />
      )}
    </>
  );
}

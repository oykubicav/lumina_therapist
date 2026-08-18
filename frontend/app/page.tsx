"use client";

import { useEffect, useState } from "react";
import { hasConsent } from "@/lib/consent";
import { hasOnboarded } from "@/lib/profile";
import ConsentModal from "@/components/ConsentModal";
import ChatWindow from "@/components/ChatWindow";
import Landing from "@/components/Landing";
import Onboarding from "@/components/Onboarding";
import { hasDecided } from "@/lib/assessments";
import AssessmentOptInModal from "@/components/AssessmentOptInModal";
import { useAuth } from "@/hooks/useAuth";

type Stage = "landing" | "consent" | "onboarding" | "chat";

export default function Page() {
  const { isAuthenticated, loading } = useAuth();
  const [state, setState] = useState<Stage>("landing");
  const [mounted, setMounted] = useState(false);
  const [showOptIn, setShowOptIn] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!loading && isAuthenticated) {
      setState(afterConsent());
    }
  }, [loading, isAuthenticated]);

  useEffect(() => {
    if (state === "chat" && isAuthenticated && !hasDecided()) {
      const timer = setTimeout(() => setShowOptIn(true), 2500);
      return () => clearTimeout(timer);
    }
  }, [state, isAuthenticated]);

  function afterConsent(): Stage {
    if (!hasConsent()) return "consent";
    return hasOnboarded() ? "chat" : "onboarding";
  }

  if (!mounted || loading) return null;

  if (state === "onboarding") {
    return <Onboarding onDone={() => setState("chat")} />;
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
      <Landing onStart={() => setState(afterConsent())} />
      {state === "consent" && (
        <ConsentModal
          onGranted={() => setState(hasOnboarded() ? "chat" : "onboarding")}
        />
      )}
    </>
  );
}

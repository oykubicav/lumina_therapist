"use client";

import { useEffect, useState } from "react";
import { hasConsent } from "@/lib/consent";
import { hasOnboarded, syncProfileOwner } from "@/lib/profile";
import ConsentModal from "@/components/ConsentModal";
import ChatWindow from "@/components/ChatWindow";
import Landing from "@/components/Landing";
import Onboarding from "@/components/Onboarding";
import { hasDecided } from "@/lib/assessments";
import AssessmentOptInModal from "@/components/AssessmentOptInModal";
import { useAuth } from "@/hooks/useAuth";

type Stage = "landing" | "consent" | "onboarding" | "chat";

export default function Page() {
  const { isAuthenticated, loading, user } = useAuth();
  const [state, setState] = useState<Stage>("landing");
  const [mounted, setMounted] = useState(false);
  const [ownerChecked, setOwnerChecked] = useState(false);
  const [showOptIn, setShowOptIn] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  // Profil cihazda tutuluyor; hesap değişmişse öncekini taşıma.
  useEffect(() => {
    if (loading) return;
    syncProfileOwner(user?.email ?? "anon");
    setOwnerChecked(true);
  }, [loading, user?.email]);

  useEffect(() => {
    if (!loading && ownerChecked && isAuthenticated) {
      setState(nextStage());
    }
  }, [loading, ownerChecked, isAuthenticated]);

  useEffect(() => {
    if (state === "chat" && isAuthenticated && !hasDecided()) {
      const timer = setTimeout(() => setShowOptIn(true), 2500);
      return () => clearTimeout(timer);
    }
  }, [state, isAuthenticated]);

  // Onboarding yalnızca hesabı olan kullanıcıya, ilk girişinde.
  // Üyeliksiz kullanımda isim/konu sormanın karşılığı yok.
  function nextStage(): Stage {
    if (!hasConsent()) return "consent";
    if (isAuthenticated && !hasOnboarded()) return "onboarding";
    return "chat";
  }

  if (!mounted || loading || !ownerChecked) return null;

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
      <Landing onStart={() => setState(nextStage())} />
      {state === "consent" && (
        <ConsentModal
          onGranted={() =>
            setState(isAuthenticated && !hasOnboarded() ? "onboarding" : "chat")
          }
        />
      )}
    </>
  );
}

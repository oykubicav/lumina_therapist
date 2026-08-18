"use client";

import { useEffect, useState } from "react";
import { hasConsent } from "@/lib/consent";
import ConsentModal from "@/components/ConsentModal";
import ChatWindow from "@/components/ChatWindow";
import Landing from "@/components/Landing";
import { hasDecided } from "@/lib/assessments";
import AssessmentOptInModal from "@/components/AssessmentOptInModal";
import { useAuth } from "@/hooks/useAuth";

export default function Page() {
  const { isAuthenticated, loading } = useAuth();
  const [state, setState] = useState<"landing" | "consent" | "chat">("landing");
  const [mounted, setMounted] = useState(false);
  const [showOptIn, setShowOptIn] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  // Giriş yapmış kullanıcı pazarlama sayfasını görmez, doğrudan sohbete girer.
  useEffect(() => {
    if (!loading && isAuthenticated) {
      setState(hasConsent() ? "chat" : "consent");
    }
  }, [loading, isAuthenticated]);

  // Ölçüm teklifi yalnızca hesabı olanlara — anonim oturumda veri kalıcı değil.
  useEffect(() => {
    if (state === "chat" && isAuthenticated && !hasDecided()) {
      const timer = setTimeout(() => setShowOptIn(true), 2500);
      return () => clearTimeout(timer);
    }
  }, [state, isAuthenticated]);

  if (!mounted || loading) {
    return null;
  }

  function handleStart() {
    setState(hasConsent() ? "chat" : "consent");
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
      <Landing onStart={handleStart} />
      {state === "consent" && (
        <ConsentModal onGranted={() => setState("chat")} />
      )}
    </>
  );
}

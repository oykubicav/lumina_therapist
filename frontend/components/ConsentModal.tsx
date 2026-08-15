"use client";

import { useEffect, useState } from "react";
import { Shield, Phone, Database, AlertTriangle } from "lucide-react";
import { hasConsent, grantConsent } from "@/lib/consent";
import { getSessionId, setSessionId } from "@/lib/session";
import { postConsent } from "@/lib/api";

const POLICY_VERSION = "0.2";

export default function ConsentModal({
  onGranted,
}: {
  onGranted?: () => void;
}) {
  const [open, setOpen] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!hasConsent()) setOpen(true);
  }, []);

  async function handleAccept() {
    setBusy(true);
    setError(null);
    try {
      const existing = getSessionId() || undefined;
      const res = await postConsent(POLICY_VERSION, existing);
      setSessionId(res.session_id);
      grantConsent();
      setOpen(false);
      onGranted?.();
    } catch (e: any) {
      console.error("consent backend call failed", e);
      setError(
        "Onay kayıt sunucusuna ulaşılamadı. Onayın yerelde kaydedildi; sonraki kullanımda tekrar denenecek."
      );
      grantConsent();
      setSessionId("");
      setTimeout(() => {
        setOpen(false);
        onGranted?.();
      }, 1500);
    } finally {
      setBusy(false);
    }
  }

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-black/40 dark:bg-black/60 backdrop-blur-sm p-4 animate-fade-in">
      <div className="w-full max-w-md rounded-2xl bg-cbt-surface dark:bg-cbt-dark-surface shadow-modal p-6 sm:p-7 animate-modal-in border border-cbt-border/40 dark:border-cbt-dark-border/40">
        <div className="flex items-center gap-3 mb-5">
          <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-cbt-accentSoft dark:bg-cbt-dark-accentSoft">
            <Shield
              size={18}
              className="text-cbt-accent dark:text-cbt-dark-accent"
              strokeWidth={2.2}
            />
          </div>
          <h2 className="text-lg font-semibold tracking-tight text-cbt-text dark:text-cbt-dark-text">
            Kullanım hakkında
          </h2>
        </div>

        <div className="space-y-4">
          <InfoBlock
            icon={<AlertTriangle size={15} strokeWidth={2.2} />}
            iconColor="text-cbt-warning dark:text-cbt-dark-warning"
            iconBg="bg-cbt-warningSoft dark:bg-cbt-dark-warningSoft"
          >
            <p className="text-[13px] text-cbt-text dark:text-cbt-dark-text leading-relaxed">
              Bu sohbet aracı{" "}
              <span className="font-medium">terapist, hekim ya da acil servis</span>{" "}
              yerine geçmez. Tanı koymaz, ilaç önermez ve klinik değerlendirme yapmaz.
            </p>
          </InfoBlock>

          <InfoBlock
            icon={<Phone size={15} strokeWidth={2.2} />}
            iconColor="text-cbt-danger dark:text-cbt-dark-danger"
            iconBg="bg-cbt-dangerSoft dark:bg-cbt-dark-dangerSoft"
          >
            <p className="text-[13px] text-cbt-text dark:text-cbt-dark-text leading-relaxed">
              Kriz durumundaysan (kendine ya da başkasına zarar verme düşüncesi,
              tıbbi acil belirti, aktif istismar), lütfen{" "}
              <span className="font-semibold">112</span>'yi ara ya da en yakın
              acil servise git.
            </p>
          </InfoBlock>

          <InfoBlock
            icon={<Database size={15} strokeWidth={2.2} />}
            iconColor="text-cbt-accent dark:text-cbt-dark-accent"
            iconBg="bg-cbt-accentSoft dark:bg-cbt-dark-accentSoft"
          >
            <p className="text-[13px] text-cbt-text dark:text-cbt-dark-text leading-relaxed">
              Yazdığın mesajın ham hâli kalıcı olarak saklanmaz; oturum süresince
              tutulur ve istediğin an silinebilir.
            </p>
          </InfoBlock>

          <p className="text-xs text-cbt-textMuted dark:text-cbt-dark-textMuted pt-1">
            Devam ederek yukarıdaki koşulları kabul ettiğini belirtmiş olursun.
          </p>
        </div>

        {error && (
          <div className="mt-4 flex items-start gap-2 text-xs text-cbt-warning dark:text-cbt-dark-warning bg-cbt-warningSoft dark:bg-cbt-dark-warningSoft border border-cbt-warning/20 dark:border-cbt-dark-warning/30 rounded-lg px-3 py-2">
            <AlertTriangle
              size={13}
              strokeWidth={2.2}
              className="flex-shrink-0 mt-0.5"
            />
            <p className="leading-relaxed">{error}</p>
          </div>
        )}

        <button
          className="mt-6 w-full py-2.5 rounded-xl bg-cbt-accent dark:bg-cbt-dark-accent text-white dark:text-cbt-dark-bg font-medium text-[15px] hover:bg-cbt-accentHover dark:hover:bg-cbt-dark-accentHover disabled:opacity-50 disabled:cursor-not-allowed transition-all active:scale-[0.98]"
          onClick={handleAccept}
          disabled={busy}
        >
          {busy ? "Kaydediliyor…" : "Kabul ediyorum ve devam et"}
        </button>
      </div>
    </div>
  );
}

function InfoBlock({
  children,
  icon,
  iconColor,
  iconBg,
}: {
  children: React.ReactNode;
  icon: React.ReactNode;
  iconColor: string;
  iconBg: string;
}) {
  return (
    <div className="flex gap-3">
      <div
        className={`flex-shrink-0 flex items-center justify-center w-7 h-7 rounded-lg ${iconBg} ${iconColor}`}
      >
        {icon}
      </div>
      <div className="flex-1 pt-0.5">{children}</div>
    </div>
  );
}

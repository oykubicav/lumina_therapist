"use client";
import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { postVerify, postResendVerify } from "@/lib/api";
import { Loader2, CheckCircle, XCircle } from "lucide-react";

export default function VerifyPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen flex items-center justify-center bg-cbt-bg dark:bg-cbt-dark-bg p-6">
          <Loader2 className="animate-spin text-cbt-textMuted" size={28} strokeWidth={1.8} />
        </div>
      }
    >
      <VerifyContent />
    </Suspense>
  );
}

function VerifyContent() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token");
  const [status, setStatus] = useState<"loading" | "success" | "error">("loading");
  const [error, setError] = useState("");

  useEffect(() => {
    if (!token) {
      setStatus("error");
      setError("Doğrulama bağlantısı eksik ya da hatalı.");
      return;
    }
    postVerify(token)
      .then(() => setStatus("success"))
      .catch((err) => {
        setStatus("error");
        setError(err?.message || "Doğrulama tamamlanamadı.");
      });
  }, [token]);

  return (
    <div className="min-h-screen flex flex-col bg-cbt-bg dark:bg-cbt-dark-bg">
      <header className="px-6 py-5">
        <Link
          href="/"
          className="text-[17px] font-semibold tracking-tight text-cbt-text dark:text-cbt-dark-text"
        >
          Neva
        </Link>
      </header>

      <main className="flex-1 flex items-center justify-center px-6 pb-24">
        <div className="max-w-sm text-center">
          {status === "loading" && (
            <>
              <Loader2
                className="animate-spin mx-auto mb-6 text-cbt-textMuted"
                size={28}
                strokeWidth={1.8}
              />
              <p className="text-[14px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary">
                E-postan doğrulanıyor…
              </p>
            </>
          )}

          {status === "success" && (
            <>
              <CheckCircle
                size={44}
                strokeWidth={1.5}
                className="mx-auto mb-6 text-cbt-success dark:text-cbt-dark-success"
              />
              <h2 className="text-[24px] font-semibold tracking-tight text-cbt-text dark:text-cbt-dark-text mb-3">
                E-postan doğrulandı
              </h2>
              <p className="text-[14px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary mb-8">
                Her şey hazır. Artık giriş yapabilirsin.
              </p>
              <Link
                href="/login"
                className="inline-flex items-center justify-center px-7 h-12 rounded-xl bg-cbt-text dark:bg-cbt-dark-text text-cbt-bg dark:text-cbt-dark-bg text-[15px] font-medium hover:opacity-85 transition-opacity"
              >
                Giriş yap
              </Link>
            </>
          )}

          {status === "error" && (
            <>
              <XCircle
                size={44}
                strokeWidth={1.5}
                className="mx-auto mb-6 text-cbt-danger dark:text-cbt-dark-danger"
              />
              <h2 className="text-[24px] font-semibold tracking-tight text-cbt-text dark:text-cbt-dark-text mb-3">
                Bağlantı geçersiz
              </h2>
              <p className="text-[14px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary leading-relaxed mb-6">
                {error || "Bu bağlantının süresi dolmuş ya da daha önce kullanılmış olabilir."}
              </p>

              <ResendVerifyBlock />

              <p className="text-[13px] text-cbt-textMuted dark:text-cbt-dark-textMuted mt-8">
                Sorun devam ederse{" "}
                <Link
                  href="/register"
                  className="font-medium text-cbt-text dark:text-cbt-dark-text hover:underline underline-offset-2"
                >
                  yeniden kayıt olabilirsin
                </Link>
                .
              </p>
            </>
          )}
        </div>
      </main>
    </div>
  );
}

function ResendVerifyBlock() {
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);
  const [sending, setSending] = useState(false);

  const handleResend = async (e: React.FormEvent) => {
    e.preventDefault();
    setSending(true);
    try {
      await postResendVerify(email);
      setSent(true);
    } finally {
      setSending(false);
    }
  };

  if (sent) {
    return (
      <p className="text-[14px] text-cbt-success dark:text-cbt-dark-success">
        Yeni doğrulama bağlantısı gönderildi. E-posta kutunu kontrol et.
      </p>
    );
  }

  return (
    <form onSubmit={handleResend} className="space-y-3 text-left">
      <p className="text-[13px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary text-center">
        E-posta adresini yaz, yeni bir bağlantı gönderelim:
      </p>
      <input
        type="email"
        required
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="ornek@eposta.com"
        className="w-full px-4 h-12 rounded-xl border border-cbt-border dark:border-cbt-dark-border bg-cbt-surface dark:bg-cbt-dark-surface text-[15px] text-cbt-text dark:text-cbt-dark-text placeholder:text-cbt-textMuted focus:outline-none focus:border-cbt-borderStrong dark:focus:border-cbt-dark-borderStrong transition-colors"
      />
      <button
        type="submit"
        disabled={sending || !email}
        className="w-full h-12 rounded-xl bg-cbt-text dark:bg-cbt-dark-text text-cbt-bg dark:text-cbt-dark-bg text-[15px] font-medium hover:opacity-85 transition-opacity disabled:opacity-40"
      >
        {sending ? "Gönderiliyor…" : "Yeni bağlantı gönder"}
      </button>
    </form>
  );
}

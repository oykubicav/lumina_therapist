"use client";
import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { postVerify } from "@/lib/api";
import { Loader2, CheckCircle, XCircle } from "lucide-react";
import { postResendVerify } from "@/lib/api";

// Next.js 14 requires useSearchParams to be inside a Suspense boundary
// during static generation. Wrap the actual logic in a child component.
export default function VerifyPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center bg-cbt-bg dark:bg-cbt-dark-bg p-4">
        <Loader2 className="animate-spin text-cbt-accent" size={32} />
      </div>
    }>
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
            setError("Doğrulama tokeni eksik.");
            return;
        }
        postVerify(token)
            .then(() => {
                setStatus("success");
            }
        )
        .catch((err) => {
            setStatus("error");
            setError(err?.message || "Doğrulama başarısız oldu.");
        });
    },[token]);

return (
    <div className="min-h-screen flex items-center justify-center bg-cbt-bg dark:bg-cbt-dark-bg p-4">
      <div className="max-w-md text-center">
        {status === "loading" && (
          <>
            <Loader2 className="animate-spin mx-auto mb-4 text-cbt-accent" size={32} />
            <p className="text-cbt-textSecondary">Doğrulanıyor...</p>
          </>
        )}

        {status === "success" && (
          <>
            <CheckCircle className="mx-auto mb-4 text-emerald-500" size={48} />
            <h2 className="text-xl font-medium text-cbt-text dark:text-cbt-dark-text mb-3">
              E-postan doğrulandı
            </h2>
            <p className="text-sm text-cbt-textSecondary mb-6">
              Artık giriş yapabilirsin.
            </p>
            <Link href="/login" className="inline-block px-6 py-3 rounded-xl bg-cbt-accent text-white font-medium">
              Giriş yap
            </Link>
          </>
        )}

        {status === "error" && (
  <>
    <XCircle className="mx-auto mb-4 text-red-500" size={48} />
    <h2 className="text-xl font-medium mb-3">Doğrulama başarısız</h2>
    <p className="text-sm text-red-600 mb-4">{error || "Link geçersiz ya da süresi dolmuş."}</p>

    <ResendVerifyBlock />

    <p className="text-xs text-cbt-textMuted mt-6">
      Hala sorun yaşıyorsan <Link href="/register" className="text-cbt-accent hover:underline">yeniden kayıt olabilirsin</Link>.
    </p>
  </>
)}
      </div>
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
      <p className="text-sm text-emerald-600 mt-4">
        ✓ Yeni doğrulama linki gönderildi. E-postanı kontrol et.
      </p>
    );
  }

  return (
    <form onSubmit={handleResend} className="mt-4 space-y-2">
      <p className="text-sm text-cbt-textSecondary mb-2">
        E-postanı gir, yeni bir doğrulama linki yollayalım:
      </p>
      <input
        type="email"
        required
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="you@example.com"
        className="w-full px-3 py-2 rounded-lg border border-cbt-border bg-transparent focus:outline-none focus:border-cbt-accent"
      />
      <button
        type="submit"
        disabled={sending || !email}
        className="w-full py-2 rounded-lg bg-cbt-accent text-white text-sm font-medium disabled:opacity-50"
      >
        {sending ? "Gönderiliyor..." : "Yeni link yolla"}
      </button>
    </form>
  );
}

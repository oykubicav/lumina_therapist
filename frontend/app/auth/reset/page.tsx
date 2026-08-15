"use client";

import { useState, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { postResetPassword } from "@/lib/api";
import { Loader2 } from "lucide-react";

// Next.js 14 static prerender fix: wrap useSearchParams in Suspense.
export default function ResetPasswordPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center bg-cbt-bg dark:bg-cbt-dark-bg p-4">
        <Loader2 className="animate-spin text-cbt-accent" size={32} />
      </div>
    }>
      <ResetPasswordContent />
    </Suspense>
  );
}

function ResetPasswordContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const token = searchParams.get("token") || "";
  const [newPassword, setNewPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [done, setDone] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (newPassword !== confirm) {
      setError("Şifreler eşleşmiyor");
      return;
    }
    if (!token) {
      setError("Geçersiz link");
      return;
    }

    setSubmitting(true);
    try {
        await postResetPassword(token, newPassword);
        setDone(true);
    } catch (err: any) {
      setError(err?.message || "Şifre güncellenemedi");
    } finally {
      setSubmitting(false);
    }
  };

  if (done) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-cbt-bg dark:bg-cbt-dark-bg p-4">
        <div className="max-w-md text-center">
          <h2 className="text-xl font-medium mb-3">Şifren güncellendi</h2>
          <Link href="/login" className="inline-block px-6 py-3 rounded-xl bg-cbt-accent text-white font-medium">
            Giriş yap
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-cbt-bg dark:bg-cbt-dark-bg p-4">
      <div className="w-full max-w-md">
        <h1 className="text-2xl font-medium text-center mb-2">Yeni şifre belirle</h1>
        <form onSubmit={handleSubmit} className="bg-white dark:bg-cbt-dark-surface rounded-2xl p-6 shadow-soft space-y-4 mt-6">
          <div>
            <label className="block text-xs text-cbt-textMuted mb-1">Yeni şifre</label>
            <input
              type="password"
              required
              minLength={8}
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              className="w-full px-3 py-2 rounded-lg border border-cbt-border bg-transparent focus:outline-none focus:border-cbt-accent"
            />
          </div>
          <div>
            <label className="block text-xs text-cbt-textMuted mb-1">Şifreyi tekrar yaz</label>
            <input
              type="password"
              required
              value={confirm}
              onChange={(e) => setConfirm(e.target.value)}
              className="w-full px-3 py-2 rounded-lg border border-cbt-border bg-transparent focus:outline-none focus:border-cbt-accent"
            />
          </div>
          {error && <p className="text-sm text-red-600">{error}</p>}
          <button
            type="submit"
            disabled={submitting}
            className="w-full py-3 rounded-xl bg-cbt-accent text-white font-medium disabled:opacity-50"
          >
            {submitting ? "Güncelleniyor..." : "Şifreyi kaydet"}
          </button>
        </form>
      </div>
    </div>
  );
}
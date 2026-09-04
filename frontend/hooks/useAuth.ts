"use client";

import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import {
  getToken, setToken, clearToken,
  getStoredUser, setStoredUser,
} from "@/lib/auth";
import { postLogin, postRegister, getMe, deleteMe, patchMyProfile, ApiError } from "@/lib/api";
import { clearSessionId } from "@/lib/session";
import { clearProfile } from "@/lib/profile";
import type { AuthUser, ProfileUpdate } from "@/lib/types";

export function useAuth() {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  // Mount olduğunda localStorage'dan restore et
  useEffect(() => {
    const stored = getStoredUser();
    if (stored && getToken()) {
      setUser(stored);
      // Arka planda backend'den taze user info çek (verify token hala geçerli mi)
      getMe()
        .then((fresh) => {
          setUser(fresh);
          setStoredUser(fresh);
        })
        .catch((err) => {
          // Yalnızca kimlik doğrulama hatası çıkış yaptırır. Render ücretsiz
          // katmanda uykudan kalkarken istek zaman aşımına uğrayabiliyor;
          // bunu "token geçersiz" saymak kullanıcıyı sessizce düşürüyordu.
          if (err instanceof ApiError && (err.status === 401 || err.status === 403)) {
            clearToken();
            setUser(null);
          }
        });
    }
    setLoading(false);
  }, []);
  const login = useCallback(async (email: string, password: string) => {
    const response = await postLogin(email, password);
    setToken(response.access_token);
    setStoredUser(response.user);
    setUser(response.user);
    clearSessionId(); // Yeni login olduğunda session resetlenir
  }, []);
  const register = useCallback(async (email: string, password: string) => {
  return await postRegister(email, password);   // caller kullanmak isterse
}, []);
const logout = useCallback(() => {
    clearToken();
    clearSessionId();
    clearProfile();
    setUser(null);
    router.push("/");
  }, [router]);
const deleteAccount = useCallback(async () => {
    await deleteMe();
    clearToken();
    clearSessionId();
    clearProfile();
    setUser(null);
    router.push("/");
  }, [router]);
  // Onboarding tercihlerini sunucuya yazar ve döndürdüğü kullanıcıyı state'e
  // koyar. Önbellek yukarıdaki efektle kendiliğinden eşitleniyor.
  const updateProfile = useCallback(async (req: ProfileUpdate) => {
    const fresh = await patchMyProfile(req);
    setStoredUser(fresh);
    setUser(fresh);
    return fresh;
  }, []);

  return {
    user,
    loading,
    isAuthenticated: !!user,
    login,
    register,
    logout,
    deleteAccount,
    updateProfile,
  };
}

    













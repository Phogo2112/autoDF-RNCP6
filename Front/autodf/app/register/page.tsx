"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { motion } from "framer-motion";
import authService from "../src/service/authService";

export default function RegisterPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    name_business: "",
    siret: "",
  });
  const [error, setError] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      await authService.register(formData);
      router.push("/");
      router.refresh();
    } catch (err: any) {
      setError(err.response?.data || { detail: "Une erreur est survenue lors de l'inscription." });
    } finally {
      setIsLoading(false);
    }
  };

  const getErrorMsg = (field: string) => {
    if (error && error[field]) {
      return Array.isArray(error[field]) ? error[field][0] : error[field];
    }
    return null;
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 p-4 relative overflow-hidden py-12">
      {/* Background elements */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-0">
        <div className="absolute top-[-10%] right-[-10%] w-[40%] h-[40%] bg-cyan-500/10 blur-[120px] rounded-full"></div>
        <div className="absolute bottom-[-10%] left-[-10%] w-[40%] h-[40%] bg-purple-500/10 blur-[120px] rounded-full"></div>
      </div>

      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-lg z-10"
      >
        <div className="bg-slate-900/50 backdrop-blur-xl border border-white/10 p-8 rounded-2xl shadow-2xl">
          <div className="text-center mb-10">
            <h1 className="text-4xl font-bold bg-linear-to-r from-cyan-400 via-blue-400 to-purple-400 bg-clip-text text-transparent mb-2">
              Inscription
            </h1>
            <p className="text-slate-400">Créez votre compte autoDF en quelques secondes</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Nom de l'entreprise</label>
                <input
                  type="text"
                  required
                  className="w-full bg-slate-800/50 border border-white/5 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-cyan-500/50 transition-all"
                  placeholder="Ma Super Entreprise"
                  value={formData.name_business}
                  onChange={(e) => setFormData({ ...formData, name_business: e.target.value })}
                />
                {getErrorMsg("name_business") && <p className="text-red-400 text-xs mt-1">{getErrorMsg("name_business")}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">SIRET</label>
                <input
                  type="text"
                  required
                  maxLength={14}
                  className="w-full bg-slate-800/50 border border-white/5 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-cyan-500/50 transition-all"
                  placeholder="12345678901234"
                  value={formData.siret}
                  onChange={(e) => setFormData({ ...formData, siret: e.target.value })}
                />
                {getErrorMsg("siret") && <p className="text-red-400 text-xs mt-1">{getErrorMsg("siret")}</p>}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Email</label>
              <input
                type="email"
                required
                className="w-full bg-slate-800/50 border border-white/5 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-cyan-500/50 transition-all"
                placeholder="contact@entreprise.com"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              />
              {getErrorMsg("email") && <p className="text-red-400 text-xs mt-1">{getErrorMsg("email")}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Mot de passe</label>
              <input
                type="password"
                required
                className="w-full bg-slate-800/50 border border-white/5 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-cyan-500/50 transition-all"
                placeholder="••••••••"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              />
              {getErrorMsg("password") && <p className="text-red-400 text-xs mt-1">{getErrorMsg("password")}</p>}
            </div>

            {error && error.detail && (
              <p className="text-red-400 text-sm bg-red-400/10 border border-red-400/20 p-3 rounded-lg text-center">
                {error.detail}
              </p>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-linear-to-r from-cyan-500 via-blue-500 to-purple-500 text-white font-bold py-3 rounded-lg hover:shadow-lg hover:shadow-cyan-500/25 transition-all active:scale-95 disabled:opacity-50 mt-4"
            >
              {isLoading ? "Création du compte..." : "S'inscrire"}
            </button>
          </form>

          <div className="mt-8 text-center text-slate-400 text-sm">
            Déjà un compte ?{" "}
            <Link href="/login" className="text-cyan-400 hover:underline">
              Connectez-vous
            </Link>
          </div>
        </div>
      </motion.div>
    </div>
  );
}

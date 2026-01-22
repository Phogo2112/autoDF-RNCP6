'use client';
import { useState, useEffect, } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { AnimatePresence, motion } from "framer-motion";
import authService from "../app/src/service/authService";

export default function Navbar() {
  const router = useRouter();
  const [isOpen, setIsOpen] = useState(false);
  const [activeLink, setActiveLink] = useState("/");
  const [isAuth, setIsAuth] = useState(false);

  useEffect(() => {
    setIsAuth(authService.isAuthenticated());
  }, []);

  const handleLogout = () => {
    authService.logout();
    setIsAuth(false);
    router.push("/login");
  };

  const navLinks = [
    { href: "/", label: "Accueil" },
    { href: "/estimate", label: "Devis" },
    { href: "/invoice", label: "Factures" },
    { href: "/home", label: "Dashboard" },
    { href: "/login", label: "Se connecter" },
    { href: "/register", label: "S'inscrire" },
    { href: "/logout", label: "Se deconnecter" },
  ];

  return (
    <>
      <motion.nav
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
        className="fixed top-0 left-0 right-0 z-50 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 backdrop-blur-xl border-b border-white/10 shadow-2xl"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            {/* Logo */}
            <motion.div
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="flex items-center space-x-3"
            >
              <Link href="/" onClick={() => setActiveLink("/")}>
                <div className="relative group cursor-pointer">
                  <div className="absolute -inset-2 bg-gradient-to-r from-cyan-500 via-blue-500 to-purple-500 rounded-lg blur opacity-30 group-hover:opacity-60 transition duration-300"></div>
                  <div className="relative flex items-center space-x-3 bg-slate-900 px-4 py-2 rounded-lg border border-white/10">
                    <svg
                      className="w-8 h-8 text-cyan-400"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                      />
                    </svg>
                    <span className="text-2xl font-bold bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-400 bg-clip-text text-transparent">
                      autoDF
                    </span>
                  </div>
                </div>
              </Link>
            </motion.div>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center space-x-1">
              {navLinks.map((link, index) => (
                <motion.div
                  key={link.href}
                  initial={{ opacity: 0, y: -20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1, duration: 0.5 }}
                >
                  <Link
                    href={link.href}
                    onClick={() => setActiveLink(link.href)}
                    className="relative group"
                  >
                    <span
                      className={`
                      px-5 py-2.5 rounded-lg text-sm font-medium transition-all duration-300
                      ${activeLink === link.href
                          ? "text-white bg-white/10"
                          : "text-gray-300 hover:text-white hover:bg-white/5"
                        }
                    `}
                    >
                      {link.label}
                    </span>
                    {activeLink === link.href && (
                      <motion.div
                        layoutId="activeNav"
                        className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-400"
                        transition={{
                          type: "spring",
                          stiffness: 380,
                          damping: 30,
                        }}
                      />
                    )}
                  </Link>
                </motion.div>
              ))}
            </div>

            {/* Authentication / CTA */}
            <div className="hidden md:flex items-center space-x-4">
              {isAuth ? (
                <>
                  <motion.div
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.4, duration: 0.5 }}
                  >
                    <button className="relative group overflow-hidden px-6 py-2.5 rounded-lg font-medium text-white transition-all duration-300">
                      <div className="absolute inset-0 bg-linear-to-r from-cyan-500 via-blue-500 to-purple-500 transition-transform duration-300 group-hover:scale-105"></div>
                      <span className="relative flex items-center space-x-2">
                        <span>Nouveau document</span>
                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                        </svg>
                      </span>
                    </button>
                  </motion.div>

                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleLogout}
                    className="text-gray-400 hover:text-white px-4 py-2 text-sm font-medium transition-colors"
                  >
                    Déconnexion
                  </motion.button>
                </>
              ) : (
                <div className="flex items-center space-x-2">
                  <Link href="/login">
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      className="text-gray-300 hover:text-white px-4 py-2 text-sm font-medium transition-colors"
                    >
                      Connexion
                    </motion.button>
                  </Link>
                  <Link href="/register">
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      className="bg-linear-to-r from-cyan-500 to-blue-500 text-white px-5 py-2 rounded-lg text-sm font-medium shadow-lg shadow-cyan-500/20"
                    >
                      S'inscrire
                    </motion.button>
                  </Link>
                </div>
              )}
            </div>

            {/* Mobile menu button */}
            <motion.button
              whileTap={{ scale: 0.9 }}
              onClick={() => setIsOpen(!isOpen)}
              className="md:hidden relative z-50 w-10 h-10 flex items-center justify-center rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
            >
              <div className="w-6 h-5 flex flex-col justify-between">
                <motion.span
                  animate={isOpen ? { rotate: 45, y: 8 } : { rotate: 0, y: 0 }}
                  className="w-full h-0.5 bg-white rounded-full transition-all"
                />
                <motion.span
                  animate={isOpen ? { opacity: 0 } : { opacity: 1 }}
                  className="w-full h-0.5 bg-white rounded-full transition-all"
                />
                <motion.span
                  animate={
                    isOpen ? { rotate: -45, y: -8 } : { rotate: 0, y: 0 }
                  }
                  className="w-full h-0.5 bg-white rounded-full transition-all"
                />
              </div>
            </motion.button>
          </div>
        </div>

        {/* Mobile Menu */}
        <AnimatePresence>
          {isOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.3 }}
              className="md:hidden border-t border-white/10 bg-slate-900/95 backdrop-blur-xl"
            >
              <div className="px-4 py-6 space-y-3">
                {navLinks.map((link, index) => (
                  <motion.div
                    key={link.href}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <Link
                      href={link.href}
                      onClick={() => {
                        setActiveLink(link.href);
                        setIsOpen(false);
                      }}
                      className={`
                        block px-4 py-3 rounded-lg text-base font-medium transition-all
                        ${activeLink === link.href
                          ? "bg-gradient-to-r from-cyan-500/20 via-blue-500/20 to-purple-500/20 text-white border border-white/10"
                          : "text-gray-300 hover:bg-white/5 hover:text-white"
                        }
                      `}
                    >
                      {link.label}
                    </Link>
                  </motion.div>
                ))}
                {isAuth ? (
                  <>
                    <motion.button
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.4 }}
                      className="w-full mt-4 px-4 py-3 rounded-lg bg-linear-to-r from-cyan-500 via-blue-500 to-purple-500 text-white font-medium hover:shadow-lg hover:shadow-blue-500/50 transition-all"
                    >
                      Nouveau document
                    </motion.button>
                    <button
                      onClick={handleLogout}
                      className="w-full mt-2 px-4 py-3 rounded-lg bg-white/5 text-gray-300 font-medium hover:bg-white/10 transition-all text-left"
                    >
                      Déconnexion
                    </button>
                  </>
                ) : (
                  <div className="pt-4 space-y-2">
                    <Link href="/login" className="block" onClick={() => setIsOpen(false)}>
                      <button className="w-full px-4 py-3 rounded-lg bg-white/5 text-white font-medium border border-white/10">
                        Connexion
                      </button>
                    </Link>
                    <Link href="/register" className="block" onClick={() => setIsOpen(false)}>
                      <button className="w-full px-4 py-3 rounded-lg bg-linear-to-r from-cyan-500 to-blue-500 text-white font-medium">
                        S'inscrire
                      </button>
                    </Link>
                  </div>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.nav>

      {/* Spacer to prevent content from hiding under fixed navbar */}
      <div className="h-20"></div>
    </>
  );
}

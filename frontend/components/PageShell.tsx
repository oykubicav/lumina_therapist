import Link from "next/link";
import SiteFooter from "./SiteFooter";

export default function PageShell({
  title,
  intro,
  children,
}: {
  title: string;
  intro?: string;
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen flex flex-col bg-cbt-bg dark:bg-cbt-dark-bg">
      <header className="sticky top-0 z-20 border-b border-cbt-border/50 dark:border-cbt-dark-border/50 bg-cbt-bg/80 dark:bg-cbt-dark-bg/80 backdrop-blur-xl">
        <div className="max-w-3xl mx-auto flex items-center justify-between px-6 py-4">
          <Link
            href="/"
            className="text-[17px] font-semibold tracking-tight text-cbt-text dark:text-cbt-dark-text"
          >
            Neva
          </Link>
          <Link
            href="/"
            className="text-[13px] font-medium text-cbt-textSecondary dark:text-cbt-dark-textSecondary hover:text-cbt-text dark:hover:text-cbt-dark-text transition-colors"
          >
            Sohbete git
          </Link>
        </div>
      </header>

      <main className="flex-1 max-w-3xl w-full mx-auto px-6 pt-16 pb-24">
        <h1 className="text-[38px] sm:text-[46px] font-semibold tracking-[-0.02em] text-cbt-text dark:text-cbt-dark-text leading-[1.1] mb-5">
          {title}
        </h1>
        {intro && (
          <p className="text-[18px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary leading-relaxed mb-14">
            {intro}
          </p>
        )}
        <div className="space-y-12">{children}</div>
      </main>

      <SiteFooter />
    </div>
  );
}

export function Block({
  id,
  heading,
  children,
}: {
  id?: string;
  heading: string;
  children: React.ReactNode;
}) {
  return (
    <section id={id} className="scroll-mt-24">
      <h2 className="text-[22px] font-semibold tracking-tight text-cbt-text dark:text-cbt-dark-text mb-4">
        {heading}
      </h2>
      <div className="space-y-4 text-[15px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary leading-[1.7]">
        {children}
      </div>
    </section>
  );
}

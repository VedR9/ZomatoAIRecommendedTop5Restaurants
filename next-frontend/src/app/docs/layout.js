"use client";
import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

const navLinks = [
  { href: '/docs/setup', label: 'Setup Guide' },
  { href: '/docs/architecture', label: 'Architecture' },
  { href: '/docs/problem-statement', label: 'Problem Statement' },
  { href: '/docs/deployment', label: 'Deployment & Cost' },
  { href: '/docs/roadmap', label: 'Roadmap & Checklist' },
];

export default function DocsLayout({ children }) {
  const pathname = usePathname();

  return (
    <div style={{ display: 'flex', minHeight: '100vh', background: 'var(--bg-color)' }}>
      <aside style={{
        width: '240px',
        flexShrink: 0,
        background: 'var(--card-bg)',
        borderRight: '1px solid var(--border-color)',
        padding: '2rem 1.5rem',
        position: 'sticky',
        top: 0,
        height: '100vh',
        overflowY: 'auto',
      }}>
        <h2 style={{ margin: '0 0 0.25rem 0', fontSize: '1.1rem', fontWeight: 800 }}>Phase 7 Docs</h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', margin: '0 0 2rem 0' }}>Handoff & Documentation</p>
        <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          {navLinks.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              style={{
                color: pathname === href ? 'var(--primary-accent)' : 'var(--text-primary)',
                textDecoration: 'none',
                padding: '0.5rem 0.75rem',
                borderRadius: '6px',
                fontSize: '0.9rem',
                background: pathname === href ? 'rgba(99,102,241,0.15)' : 'transparent',
                fontWeight: pathname === href ? 600 : 400,
                transition: 'background 0.2s',
              }}
            >
              {label}
            </Link>
          ))}
        </nav>
        <hr style={{ borderColor: 'var(--border-color)', margin: '1.5rem 0' }} />
        <Link href="/" style={{ color: 'var(--primary-accent)', textDecoration: 'none', fontWeight: 600, fontSize: '0.9rem' }}>
          ← Back to App
        </Link>
      </aside>
      <main style={{ flex: 1, padding: '3rem', maxWidth: '800px', overflowY: 'auto' }}>
        {children}
      </main>
    </div>
  );
}

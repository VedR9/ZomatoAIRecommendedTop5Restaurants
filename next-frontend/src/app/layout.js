import "./globals.css";

export const metadata = {
  title: "biteAI — AI Restaurant Recommendations",
  description: "Discover the best restaurants, personalized for your taste, mood and cravings — powered by AI.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

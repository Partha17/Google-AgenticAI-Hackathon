import MainLayout from '../../components/Layout/MainLayout';

export default function ChatLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <MainLayout>{children}</MainLayout>;
}
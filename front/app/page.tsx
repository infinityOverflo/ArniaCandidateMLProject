import Image from "next/image";
import DNDTest from "./dnd_component/dnd_comp";

export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center p-8">
      <main className="flex flex-col items-center gap-8">
        <DNDTest />
        <Image
          className="dark:invert"
          src="/next.svg"
          alt="Next.js logo"
          width={180}
          height={38}
          priority
        />
      </main>
    </div>
  );
}

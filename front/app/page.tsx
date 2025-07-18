import Image from "next/image";
import FileDrop from "./file_drop_component/file_drop_component";
import DebugButton from "./debug_component/debug_component";

export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center p-8">
      <main className="flex flex-col items-center gap-24">
        <FileDrop />
        <DebugButton />
        <Image className={`flex items-center justify-center dark:invert`}
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

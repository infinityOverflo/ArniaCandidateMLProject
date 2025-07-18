"use client"

import Image from "next/image";
import styles from "./debug.module.css";

export async function handleDebug(): Promise<any> {
    try {
        const response = await fetch("http://localhost:5000/debug", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });
    } catch (error) {
        console.error("Error occurred while debugging:", error);
    }
};

export default function DebugButton() {
    return (
        <button className={`${styles.DebugButton}`} onClick={handleDebug}>
            Debug
        </button>
    );
}

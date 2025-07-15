"use client"

import Image from "next/image";
import styles from "./file_drop.module.css";

let files = [];

interface FileDropChangeEvent extends React.ChangeEvent<HTMLInputElement> {}

function handleFileChange(event: FileDropChangeEvent): void {
    files = Array.from(event.target.files as FileList);
}

export default function FileDrop() {
    return (
        <div className={`flex items-center justify-center ${styles.fileDrop}`}>
            <label htmlFor="fileDropInput">Choose PDF or TXT files:</label>
            <input
                id="fileDropInput"
                type="file"
                content="Drop files here or click to upload"
                accept=".pdf,.txt"
                multiple
                onChange={handleFileChange}
            />
        </div>
    );
}

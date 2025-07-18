"use client"

import Image from "next/image";
import styles from "./file_drop.module.css";

let files: Array<File>;
let formData: FormData;

interface FileDropChangeEvent extends React.ChangeEvent<HTMLInputElement> {}

export function handleFileChange(event: FileDropChangeEvent): void {
    files = Array.from(event.target.files as FileList);
    formData = new FormData();
    files.forEach(file => formData.append('files', file));
}

export async function handleSendFiles(): Promise<any> {
    if (formData){
        await fetch('http://localhost:5000/upload', {
                method: 'POST',
                body: formData
            })
                .then(res => res.json())
                .then(data => console.log(data))
                .catch(err => console.log(err));
    }
}

export default function FileDrop() {
    return (
        <div className={`${styles.fileDropContainer}`}>
            <label htmlFor="fileDropInput" className={`${styles.fileDropLabel}`}>
                <p>
                    <b>Click "Browse..." to upload</b> .pdf or .txt files
                </p>
            </label>
            <input
                id="fileDropInput"
                className={`${styles.fileDropInput}`}
                type="file"
                content="Drop files here or click to upload"
                accept=".pdf,.txt"
                multiple
                onChange={handleFileChange}
            />
            <button className={`${styles.fileDropButton}`} onClick={handleSendFiles}>
                    Send Files
            </button>
        </div>
    );
}

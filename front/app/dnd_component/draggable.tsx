"use client";

import React, { useEffect, useState } from 'react';
import {useDraggable} from '@dnd-kit/core';
import {CSS} from '@dnd-kit/utilities';
import Image from 'next/image';

export default function Draggable() {
  const {attributes, listeners, setNodeRef, transform} = useDraggable({
    id: 'unique-id',
  });
  const style = {
    transform: CSS.Translate.toString(transform),
  };
  
  return (
    <button ref={setNodeRef} 
        style={{
            ...style, position: 'relative', width: 64, height: 64, padding: 0,
            border: 'none', background: 'green', zIndex: 10}} {...listeners} {...attributes}>
        <Image src="/draggable.png" alt="Draggable Item" fill style={{objectFit: 'cover', borderRadius: 8}} />
    </button>
  );
};
"use client";

import React, { useEffect, useState } from 'react';
import {useDroppable} from '@dnd-kit/core';
import {CSS} from '@dnd-kit/utilities';

import Image from 'next/image';

export default function Droppable() {
  const {setNodeRef} = useDroppable({
    id: 'unique-id',
  });
  
  return (
    <div ref={setNodeRef} 
        style={{
            position: 'relative', width: 128, height: 128, border: '2px dashed #ccc', 
            borderRadius: 8, background: 'blue', zIndex: 5 }}>
        <Image src="/droppable.png" alt="Droppable Area" fill style={{ objectFit: 'cover', borderRadius: 8 }} />
    </div>
  );
};
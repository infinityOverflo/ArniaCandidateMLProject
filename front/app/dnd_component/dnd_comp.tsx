"use client";

import React, { useEffect, useState } from 'react';
import {DndContext} from '@dnd-kit/core';
import {CSS} from '@dnd-kit/utilities';

import Draggable from './draggable';
import Droppable from './droppable';

export default function DNDTest() {
  const [mounted, setMounted] = useState(false);
  useEffect(() => {
    setMounted(true);
  }, []);
  if (!mounted) return null;
  return (
    <DndContext>
      <div className="flex gap-4">
        <Draggable />
        <Droppable />
      </div>
    </DndContext>
  );
};
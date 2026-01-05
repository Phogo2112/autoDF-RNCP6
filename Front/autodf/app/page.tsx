"use client"
import { useState, useContext } from "react";
import Image from "next/image";



export default function Home() {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;

  async function getUsers() {
    const res = await fetch(`${apiUrl}/api/users/`);
    const data = await res.json();
    return data;
  }
  return (
    <>
      <h1 className="flex items-center justify-center">Page d'acceuil</h1>
    </>
  );
}

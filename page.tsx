// Next.js Frontend (TypeScript)
// Save as app/debit-note/page.tsx

"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface FormData {
  sumInsured: number;
  basicPremiumRate: number;
  excessProtector: number;
  tl: number;
  sd: number;
  vehicleCovered: string;
}

export default function DebitNotePage() {
  const [formData, setFormData] = useState<FormData>({
    sumInsured: 0,
    basicPremiumRate: 3.5,
    excessProtector: 0,
    tl: 0,
    sd: 0,
    vehicleCovered: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === "vehicleCovered" ? value : parseFloat(value),
    }));
  };

  const handleGeneratePDF = async () => {
    const dateIssued = new Date().toLocaleDateString("en-GB");

    const response = await fetch("http://localhost:8000/generate-debit-note", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ...formData,
        date_issued: dateIssued,
      }),
    });

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `DebitNote_${formData.vehicleCovered}_${dateIssued.replace(/\//g, "-")}.pdf`;
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Generate Debit Note</h1>
      <div className="grid gap-4">
        <div className="grid gap-2">
          <Label htmlFor="sumInsured">Sum Insured</Label>
          <Input id="sumInsured" name="sumInsured" type="number" value={formData.sumInsured} onChange={handleChange} required />
        </div>
        <div className="grid gap-2">
          <Label htmlFor="basicPremiumRate">Basic Premium Rate (%)</Label>
          <Input id="basicPremiumRate" name="basicPremiumRate" type="number" value={formData.basicPremiumRate} onChange={handleChange} required />
        </div>
        <div className="grid gap-2">
          <Label htmlFor="excessProtector">Excess Protector</Label>
          <Input id="excessProtector" name="excessProtector" type="number" value={formData.excessProtector} onChange={handleChange} required />
        </div>
        <div className="grid gap-2">
          <Label htmlFor="tl">+TL</Label>
          <Input id="tl" name="tl" type="number" value={formData.tl} onChange={handleChange} required />
        </div>
        <div className="grid gap-2">
          <Label htmlFor="sd">+SD</Label>
          <Input id="sd" name="sd" type="number" value={formData.sd} onChange={handleChange} required />
        </div>
        <div className="grid gap-2">
          <Label htmlFor="vehicleCovered">Vehicle Registration</Label>
          <Input id="vehicleCovered" name="vehicleCovered" type="text" value={formData.vehicleCovered} onChange={handleChange} required />
        </div>

        <Button onClick={handleGeneratePDF} className="mt-4">
          Generate and Download PDF
        </Button>
      </div>
    </div>
  );
}

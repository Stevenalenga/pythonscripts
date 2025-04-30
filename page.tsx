"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface LineItem {
  description: string;
  units: number;
  cost_per_unit: number;
}

interface InvoiceData {
  invoice_number: string;
  bill_to: string;
  department: string;
  tax_rate: number;
  line_items: LineItem[];
}

export default function InvoicePage() {
  const [formData, setFormData] = useState<InvoiceData>({
    invoice_number: "",
    bill_to: "",
    department: "",
    tax_rate: 0.16, // Default 16% VAT
    line_items: [{ description: "", units: 1, cost_per_unit: 0 }],
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === "tax_rate" ? parseFloat(value) / 100 : value,
    }));
  };

  const handleLineItemChange = (
    index: number,
    field: keyof LineItem,
    value: string
  ) => {
    setFormData((prev) => {
      const newLineItems = [...prev.line_items];
      newLineItems[index] = {
        ...newLineItems[index],
        [field]:
          field === "description" ? value : parseFloat(value) || 0,
      };
      return { ...prev, line_items: newLineItems };
    });
  };

  const addLineItem = () => {
    setFormData((prev) => ({
      ...prev,
      line_items: [
        ...prev.line_items,
        { description: "", units: 1, cost_per_unit: 0 },
      ],
    }));
  };

  const removeLineItem = (index: number) => {
    setFormData((prev) => ({
      ...prev,
      line_items: prev.line_items.filter((_, i) => i !== index),
    }));
  };

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    try {
      setIsLoading(true);
      setError(null);

      // Validate form data
      if (!formData.invoice_number || !formData.bill_to || !formData.department) {
        throw new Error("Please fill in all required fields");
      }

      if (!formData.line_items.length || !formData.line_items[0].description) {
        throw new Error("Please add at least one line item");
      }

      const response = await fetch("http://127.0.0.1:8000/generate-invoice", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/pdf",
        },
        body: JSON.stringify({
          ...formData,
          tax_rate: Number(formData.tax_rate),
          line_items: formData.line_items.map(item => ({
            description: item.description,
            units: Number(item.units),
            cost_per_unit: Number(item.cost_per_unit)
          }))
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new Error(errorData?.detail || 'Failed to generate invoice');
      }

      const blob = await response.blob();
      if (blob.size === 0) {
        throw new Error("Generated PDF is empty");
      }

      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `invoice_${formData.invoice_number}_${new Date().toISOString().split('T')[0]}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

    } catch (error) {
      console.error("Error:", error);
      setError(error instanceof Error ? error.message : "An unknown error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Generate Invoice</h1>
      <div className="space-y-6">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <Label htmlFor="invoice_number">Invoice Number</Label>
            <Input
              id="invoice_number"
              name="invoice_number"
              value={formData.invoice_number}
              onChange={handleChange}
              required
            />
          </div>
          <div>
            <Label htmlFor="tax_rate">Tax Rate (%)</Label>
            <Input
              id="tax_rate"
              name="tax_rate"
              type="number"
              value={formData.tax_rate * 100}
              onChange={handleChange}
              required
            />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <Label htmlFor="bill_to">Bill To</Label>
            <Input
              id="bill_to"
              name="bill_to"
              value={formData.bill_to}
              onChange={handleChange}
              required
            />
          </div>
          <div>
            <Label htmlFor="department">Department</Label>
            <Input
              id="department"
              name="department"
              value={formData.department}
              onChange={handleChange}
              required
            />
          </div>
        </div>

        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="text-lg font-semibold">Line Items</h2>
            <Button onClick={addLineItem} type="button">
              Add Item
            </Button>
          </div>

          {formData.line_items.map((item, index) => (
            <div key={index} className="grid grid-cols-4 gap-4 items-end">
              <div className="col-span-2">
                <Label>Description</Label>
                <Input
                  value={item.description}
                  onChange={(e) =>
                    handleLineItemChange(index, "description", e.target.value)
                  }
                  required
                />
              </div>
              <div>
                <Label>Units</Label>
                <Input
                  type="number"
                  value={item.units}
                  onChange={(e) =>
                    handleLineItemChange(index, "units", e.target.value)
                  }
                  required
                />
              </div>
              <div>
                <Label>Cost per Unit</Label>
                <Input
                  type="number"
                  value={item.cost_per_unit}
                  onChange={(e) =>
                    handleLineItemChange(index, "cost_per_unit", e.target.value)
                  }
                  required
                />
              </div>
              {index > 0 && (
                <Button
                  onClick={() => removeLineItem(index)}
                  variant="destructive"
                  className="mt-2"
                >
                  Remove
                </Button>
              )}
            </div>
          ))}
        </div>

        {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <Button 
        onClick={handleSubmit} 
        className="w-full"
        disabled={isLoading}
      >
        {isLoading ? "Generating..." : "Generate Invoice"}
      </Button>
      </div>
    </div>
  );
}
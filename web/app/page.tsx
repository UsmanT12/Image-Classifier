"use client";

import type React from "react";

import { useEffect, useMemo, useRef, useState } from "react";
import { Upload, ImageIcon, CheckCircle, AlertCircle } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Slider } from "@/components/ui/slider";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";

type UploadStatus = "idle" | "success" | "error";

type PickedFile = {
  file: File;
  relPath: string;
};

type ApiResult = {
  accuracy: number;
  correct: number;
  wrong: number;
  total: number;
  per_class: Record<
    string,
    {
      accuracy: number;
      correct: number;
      total: number;
      trained_images: number;
    }
  >;
  misclassified: Array<{
    predicted: string;
    actual: string;
    image: string;
    class: string;
  }>;
};

export default function ImageClassifierImport() {
  const [trainingFiles, setTrainingFiles] = useState<PickedFile[]>([]);
  const [testFiles, setTestFiles] = useState<PickedFile[]>([]);
  const [trainingProgress, setTrainingProgress] = useState(0);
  const [testProgress, setTestProgress] = useState(0);
  const [trainingStatus, setTrainingStatus] = useState<UploadStatus>("idle");
  const [testStatus, setTestStatus] = useState<UploadStatus>("idle");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [processingStatus, setProcessingStatus] = useState<string | null>(null);
  const [result, setResult] = useState<ApiResult | null>(null);

  const [threshold, setThreshold] = useState(0.015);
  const [imageWidth, setImageWidth] = useState(28);
  const [imageHeight, setImageHeight] = useState(28);
  const [numClasses, setNumClasses] = useState(2);

  const apiBase = useMemo(
    () => process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000",
    [],
  );

  const pickFolder = async (kind: "training" | "test") => {
    const picker = (window as any).showDirectoryPicker as
      | undefined
      | (() => Promise<any>);
    if (!picker) {
      setProcessingStatus(
        "Your browser doesn't support folder picking. Please use a Chromium-based browser like Chrome or Edge.",
      );
      return;
    }

    setProcessingStatus(`Select your ${kind} dataset folder...`);
    const rootHandle = await picker();
    const rootName = String(
      rootHandle?.name ?? (kind === "training" ? "training" : "test"),
    );

    const results: PickedFile[] = [];
    const walk = async (dirHandle: any, prefix: string) => {
      // eslint-disable-next-line no-restricted-syntax
      for await (const [name, entry] of dirHandle.entries()) {
        if (entry.kind === "file") {
          const file = await entry.getFile();
          const relPath = `${prefix}${name}`;
          results.push({ file, relPath });
        } else if (entry.kind === "directory") {
          await walk(entry, `${prefix}${name}/`);
        }
      }
    };

    await walk(rootHandle, `${rootName}/`);

    if (results.length === 0) {
      setProcessingStatus(
        "That folder had no files. Please pick a dataset folder that contains images.",
      );
      return;
    }

    if (kind === "training") {
      setTrainingFiles(results);
      setTrainingProgress(100);
      setTrainingStatus("success");
    } else {
      setTestFiles(results);
      setTestProgress(100);
      setTestStatus("success");
    }

    setProcessingStatus(null);
  };

  const canProceed =
    trainingStatus === "success" &&
    testStatus === "success" &&
    trainingFiles.length > 0 &&
    testFiles.length > 0;

  const handleSubmit = async () => {
    if (!canProceed || isSubmitting) return;

    setIsSubmitting(true);
    setResult(null);
    setProcessingStatus("Uploading folders and running training/testing...");

    try {
      const formData = new FormData();
      for (const f of trainingFiles) {
        formData.append("training_files", f.file, f.relPath);
      }
      for (const f of testFiles) {
        formData.append("test_files", f.file, f.relPath);
      }

      formData.append("threshold", String(threshold));
      formData.append("img_width", String(imageWidth));
      formData.append("img_height", String(imageHeight));
      formData.append("num_classes", String(numClasses));

      const resp = await fetch(`${apiBase}/train-test`, {
        method: "POST",
        body: formData,
      });

      const data = (await resp.json().catch(() => null)) as any;
      if (!resp.ok) {
        throw new Error(data?.detail ?? `Request failed (${resp.status})`);
      }

      setResult(data as ApiResult);
      setProcessingStatus("Complete.");
    } catch (error) {
      setProcessingStatus(
        `Error: ${error instanceof Error ? error.message : "Unknown error occurred"}`,
      );
      setTrainingStatus("error");
      setTestStatus("error");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="container mx-auto py-10 px-4">
      <h1 className="text-3xl font-bold text-center mb-8">
        Image Classifier Setup
      </h1>

      <div className="grid md:grid-cols-2 gap-8 mb-8">
        <Card className="h-full">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <ImageIcon className="h-5 w-5" />
              Training Images
            </CardTitle>
            <CardDescription>
              Choose your training folder (it must contain class subfolders like
              cats/, dogs/)
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div
              className={`border-2 border-dashed rounded-lg p-6 text-center ${
                trainingStatus === "success"
                  ? "border-green-500 bg-green-50"
                  : trainingStatus === "error"
                    ? "border-red-500 bg-red-50"
                    : "border-gray-300 hover:border-gray-400"
              }`}
            >
              {trainingStatus === "idle" ? (
                <>
                  <Upload className="h-12 w-12 mx-auto text-gray-400 mb-4" />
                  <h3 className="text-lg font-medium mb-2">
                    Select a training folder
                  </h3>
                  <p className="text-sm text-gray-500 mb-4">
                    Your folder should contain one subfolder per class.
                  </p>
                </>
              ) : trainingStatus === "success" ? (
                <>
                  <CheckCircle className="h-12 w-12 mx-auto text-green-500 mb-4" />
                  <h3 className="text-lg font-medium mb-2">
                    Imported {trainingFiles.length} training images
                  </h3>
                  <Progress value={trainingProgress} className="mb-2" />
                </>
              ) : (
                <>
                  <AlertCircle className="h-12 w-12 mx-auto text-red-500 mb-4" />
                  <h3 className="text-lg font-medium mb-2">
                    Error importing images
                  </h3>
                  <p className="text-sm text-red-500 mb-4">
                    Please re-select the training folder.
                  </p>
                </>
              )}

              <div className="mt-4 flex flex-col items-center gap-2">
                <Button
                  type="button"
                  onClick={() => pickFolder("training")}
                  disabled={isSubmitting}
                >
                  Select Training Folder
                </Button>
                <p className="text-xs text-gray-500">
                  Recommended: uses Chrome’s folder picker and preserves
                  subfolders as class labels.
                </p>
              </div>
            </div>
          </CardContent>
          {trainingFiles.length > 0 && (
            <CardFooter className="flex-col items-start">
              <h4 className="text-sm font-medium mb-2">
                Preview ({trainingFiles.length} files)
              </h4>
              <ScrollArea className="h-28 w-full rounded border p-2">
                <div className="grid grid-cols-4 gap-2">
                  {trainingFiles.slice(0, 8).map((_, index) => (
                    <div
                      key={index}
                      className="aspect-square bg-gray-100 rounded flex items-center justify-center"
                    >
                      <ImageIcon className="h-6 w-6 text-gray-400" />
                    </div>
                  ))}
                  {trainingFiles.length > 8 && (
                    <div className="aspect-square bg-gray-100 rounded flex items-center justify-center">
                      <span className="text-sm text-gray-500">
                        +{trainingFiles.length - 8} more
                      </span>
                    </div>
                  )}
                </div>
              </ScrollArea>
            </CardFooter>
          )}
        </Card>

        <Card className="h-full">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <ImageIcon className="h-5 w-5" />
              Test Images
            </CardTitle>
            <CardDescription>
              Choose your test folder (same class subfolder structure as
              training)
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div
              className={`border-2 border-dashed rounded-lg p-6 text-center ${
                testStatus === "success"
                  ? "border-green-500 bg-green-50"
                  : testStatus === "error"
                    ? "border-red-500 bg-red-50"
                    : "border-gray-300 hover:border-gray-400"
              }`}
            >
              {testStatus === "idle" ? (
                <>
                  <Upload className="h-12 w-12 mx-auto text-gray-400 mb-4" />
                  <h3 className="text-lg font-medium mb-2">
                    Select a test folder
                  </h3>
                  <p className="text-sm text-gray-500 mb-4">
                    Your folder should contain one subfolder per class.
                  </p>
                </>
              ) : testStatus === "success" ? (
                <>
                  <CheckCircle className="h-12 w-12 mx-auto text-green-500 mb-4" />
                  <h3 className="text-lg font-medium mb-2">
                    Imported {testFiles.length} test images
                  </h3>
                  <Progress value={testProgress} className="mb-2" />
                </>
              ) : (
                <>
                  <AlertCircle className="h-12 w-12 mx-auto text-red-500 mb-4" />
                  <h3 className="text-lg font-medium mb-2">
                    Error importing images
                  </h3>
                  <p className="text-sm text-red-500 mb-4">
                    Please re-select the test folder.
                  </p>
                </>
              )}

              <div className="mt-4 flex flex-col items-center gap-2">
                <Button
                  type="button"
                  onClick={() => pickFolder("test")}
                  disabled={isSubmitting}
                >
                  Select Test Folder
                </Button>
                <p className="text-xs text-gray-500">
                  Recommended: uses Chrome’s folder picker and preserves
                  subfolders as class labels.
                </p>
              </div>
            </div>
          </CardContent>
          {testFiles.length > 0 && (
            <CardFooter className="flex-col items-start">
              <h4 className="text-sm font-medium mb-2">
                Preview ({testFiles.length} files)
              </h4>
              <ScrollArea className="h-28 w-full rounded border p-2">
                <div className="grid grid-cols-4 gap-2">
                  {testFiles.slice(0, 8).map((_, index) => (
                    <div
                      key={index}
                      className="aspect-square bg-gray-100 rounded flex items-center justify-center"
                    >
                      <ImageIcon className="h-6 w-6 text-gray-400" />
                    </div>
                  ))}
                  {testFiles.length > 8 && (
                    <div className="aspect-square bg-gray-100 rounded flex items-center justify-center">
                      <span className="text-sm text-gray-500">
                        +{testFiles.length - 8} more
                      </span>
                    </div>
                  )}
                </div>
              </ScrollArea>
            </CardFooter>
          )}
        </Card>
      </div>

      <div className="mb-8 mt-8">
        <h2 className="text-2xl font-bold mb-6">Model Configuration</h2>
        <div className="grid md:grid-cols-3 gap-8">
          <Card>
            <CardHeader>
              <CardTitle>Threshold Value</CardTitle>
              <CardDescription>0.001–1.0 (default: 0.015)</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <Label htmlFor="threshold">Threshold</Label>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="flex-1">
                      <Slider
                        id="threshold"
                        min={0.001}
                        max={1.0}
                        step={0.001}
                        value={[threshold]}
                        onValueChange={(value) => setThreshold(value[0])}
                      />
                      <div className="flex justify-between text-xs text-muted-foreground mt-1">
                        <span>0.001</span>
                        <span>0.500</span>
                        <span>1.000</span>
                      </div>
                    </div>
                    <div className="w-24">
                      <Input
                        type="number"
                        min="0.001"
                        max="1.0"
                        step="0.001"
                        value={threshold}
                        onChange={(e) => {
                          const value = Number.parseFloat(e.target.value);
                          if (!isNaN(value))
                            setThreshold(Math.min(1.0, Math.max(0.001, value)));
                        }}
                        className="text-right"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Image Size</CardTitle>
              <CardDescription>Max 128×128 (default: 28×28)</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="width">Width</Label>
                    <Input
                      id="width"
                      type="number"
                      min="1"
                      max="128"
                      value={imageWidth}
                      onChange={(e) =>
                        setImageWidth(
                          Math.min(
                            128,
                            Math.max(1, Number.parseInt(e.target.value) || 1),
                          ),
                        )
                      }
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="height">Height</Label>
                    <Input
                      id="height"
                      type="number"
                      min="1"
                      max="128"
                      value={imageHeight}
                      onChange={(e) =>
                        setImageHeight(
                          Math.min(
                            128,
                            Math.max(1, Number.parseInt(e.target.value) || 1),
                          ),
                        )
                      }
                    />
                  </div>
                </div>
                <p className="text-xs text-muted-foreground">
                  These values must match what you want to resize images to.
                </p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Number of Classes</CardTitle>
              <CardDescription>2–10 (default: 2)</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="num-classes">Classes</Label>
                  <Input
                    id="num-classes"
                    type="number"
                    min="2"
                    max="10"
                    value={numClasses}
                    onChange={(e) =>
                      setNumClasses(
                        Math.min(
                          10,
                          Math.max(2, Number.parseInt(e.target.value) || 2),
                        ),
                      )
                    }
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {canProceed ? (
        <Alert className="bg-green-50 border-green-200">
          <CheckCircle className="h-4 w-4 text-green-600" />
          <AlertTitle>Ready to proceed</AlertTitle>
          <AlertDescription>
            Both training and test folders have been imported.
          </AlertDescription>
        </Alert>
      ) : (
        <Alert>
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Import required</AlertTitle>
          <AlertDescription>
            Please import both training and test folders to continue.
          </AlertDescription>
        </Alert>
      )}

      {processingStatus && (
        <Alert
          className={
            isSubmitting
              ? "bg-blue-50 border-blue-200 mt-4"
              : "bg-yellow-50 border-yellow-200 mt-4"
          }
        >
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>{isSubmitting ? "Processing" : "Status"}</AlertTitle>
          <AlertDescription>{processingStatus}</AlertDescription>
        </Alert>
      )}

      {result && (
        <div className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Results</CardTitle>
              <CardDescription>
                Accuracy: {(result.accuracy * 100).toFixed(2)}% (
                {result.correct}/{result.total})
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="text-sm">
                <div>
                  <span className="font-medium">Correct:</span> {result.correct}
                </div>
                <div>
                  <span className="font-medium">Wrong:</span> {result.wrong}
                </div>
              </div>
              <div className="rounded border p-3">
                <div className="text-sm font-medium mb-2">
                  Per-class accuracy
                </div>
                <div className="grid md:grid-cols-2 gap-2 text-sm">
                  {Object.entries(result.per_class).map(([cls, stats]) => (
                    <div key={cls} className="flex justify-between gap-2">
                      <span className="font-medium">{cls}</span>
                      <span>
                        {(stats.accuracy * 100).toFixed(2)}% ({stats.correct}/
                        {stats.total}), trained: {stats.trained_images}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      <div className="flex justify-center mt-8">
        <Button
          size="lg"
          disabled={!canProceed || isSubmitting}
          onClick={handleSubmit}
        >
          {isSubmitting ? "Processing..." : "Start Training Classifier"}
        </Button>
      </div>
    </div>
  );
}

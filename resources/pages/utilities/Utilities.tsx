import MainLayout from "@/layouts/MainLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { StateConversionForm } from "./components/state-conversion-form";
import { TimeConversionForm } from "./components/time-conversion-form";

export default function UtilitiesPage() {
  return (
    <MainLayout
      title="Utilities"
      description="Various orbital mechanics and mission analysis tools"
      keywords="Utilities, Tools, State Conversion, Time Conversion"
    >
      <div className="container mx-auto py-8 space-y-8">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold">Utilities</h1>
        </div>

        <Tabs defaultValue="state-conversion" className="w-full">
          <TabsList>
            <TabsTrigger value="state-conversion">State Conversion</TabsTrigger>
            <TabsTrigger value="time-conversion">Time Conversion</TabsTrigger>
            {/* Add more TabsTriggers for future utilities */}
          </TabsList>

          <TabsContent value="state-conversion">
            <Card>
              <CardHeader>
                <CardTitle>State Conversion</CardTitle>
              </CardHeader>
              <CardContent>
                <StateConversionForm />
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="time-conversion">
            <Card>
              <CardHeader>
                <CardTitle>Time Conversion</CardTitle>
              </CardHeader>
              <CardContent>
                <TimeConversionForm />
              </CardContent>
            </Card>
          </TabsContent>

          {/* Add more TabsContent sections for future utilities */}
        </Tabs>
      </div>
    </MainLayout>
  );
} 
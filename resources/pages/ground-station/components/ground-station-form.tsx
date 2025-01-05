import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { Button } from "@/components/ui/button";
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";
import { GroundStation } from "@/types/ground-station";
import ElevationMaskEditor from "./elevation-mask-editor";

const formSchema = z.object({
    name: z.string().min(1, "Name is required"),
    group: z.string().optional(),
    longitude: z.number().min(-180).max(180),
    latitude: z.number().min(-90).max(90),
    altitude: z.number(),
    elevationMask: z.array(z.object({
        azimuth: z.number().min(0).max(360),
        elevation: z.number().min(0).max(90),
    })),
});

interface GroundStationFormProps {
    initialData?: GroundStation;
    onSubmit: (data: GroundStation) => Promise<void>;
    onCancel: () => void;
}

export function GroundStationForm({ initialData, onSubmit, onCancel }: GroundStationFormProps) {
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: initialData || {
            name: "",
            group: "",
            longitude: 0,
            latitude: 0,
            altitude: 0,
            elevationMask: [],
        },
    });

    const handleSubmit = async (data: z.infer<typeof formSchema>) => {
        try {
            await onSubmit(data as GroundStation);
            toast.success("Ground station saved successfully");
        } catch (error) {
            toast.error("Failed to save ground station");
        }
    };

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-4">
                <FormField
                    control={form.control}
                    name="name"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Name</FormLabel>
                            <FormControl>
                                <Input {...field} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                <FormField
                    control={form.control}
                    name="group"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Group (Optional)</FormLabel>
                            <FormControl>
                                <Input {...field} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                <div className="grid grid-cols-3 gap-4">
                    <FormField
                        control={form.control}
                        name="longitude"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Longitude (°)</FormLabel>
                                <FormControl>
                                    <Input type="number" step="0.000001" {...field} onChange={e => field.onChange(parseFloat(e.target.value))} />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />

                    <FormField
                        control={form.control}
                        name="latitude"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Latitude (°)</FormLabel>
                                <FormControl>
                                    <Input type="number" step="0.000001" {...field} onChange={e => field.onChange(parseFloat(e.target.value))} />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />

                    <FormField
                        control={form.control}
                        name="altitude"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Altitude (m)</FormLabel>
                                <FormControl>
                                    <Input type="number" step="0.1" {...field} onChange={e => field.onChange(parseFloat(e.target.value))} />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                </div>

                <ElevationMaskEditor
                    value={form.watch("elevationMask")}
                    onChange={(value) => form.setValue("elevationMask", value)}
                />

                <div className="flex justify-end space-x-2">
                    <Button variant="outline" onClick={onCancel}>
                        Cancel
                    </Button>
                    <Button type="submit">
                        {initialData ? "Update" : "Create"} Ground Station
                    </Button>
                </div>
            </form>
        </Form>
    );
} 
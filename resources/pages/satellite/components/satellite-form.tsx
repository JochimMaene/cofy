import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
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
import { Satellite } from "@/types/satellite";
import { createOrUpdateSatellite } from "@/services/satellite";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useEffect, useState } from "react";
import { Dynamics } from "@/types/dynamics";
import { fetchDynamics } from "@/services/dynamics";

// Validation schema
const satelliteSchema = z.object({
    name: z.string().min(1, "Name is required"),
    group: z.string().optional(),
    dryMass: z.number().positive("Dry mass must be positive"),
    dragArea: z.number().positive("Drag area must be positive"),
    dragCoefficient: z.number().positive("Drag coefficient must be positive"),
    srpArea: z.number().positive("SRP area must be positive"),
    srpCoefficient: z.number().positive("SRP coefficient must be positive"),
    dynamicsId: z.string().min(1, "Dynamics selection is required"),
    tleConfig: z.object({
        noradId: z.number().int().positive(),
        classification: z.enum(["U", "C"]),
        launchYear: z.number().int().min(1957).max(new Date().getFullYear()),
        launchNumber: z.number().int().positive(),
        pieceOfLaunch: z.string(),
    }),
    propulsion: z.object({
        name: z.string(),
        direction: z.string(),
        isp: z.number().positive(),
        thrustLevel: z.number().positive(),
        minBurnDuration: z.number().positive(),
        maxBurnDuration: z.number().positive(),
    }),
    aocs: z.object({
        name: z.string(),
        maximumAngVel: z.number().positive(),
    }),
    gnss: z.object({
        name: z.string(),
        posXStd: z.number().positive(),
        posYStd: z.number().positive(),
        posZStd: z.number().positive(),
        velStd: z.number().positive(),
    }),
});

type SatelliteFormValues = z.infer<typeof satelliteSchema>;

interface SatelliteFormProps {
    initialData?: Satellite;
    onRefresh: () => void;
    onClose: () => void;
}

interface FormSectionProps {
    title: string;
    fields: Array<{
        name: string;
        label: string;
        type?: "text" | "number";
    }>;
    control: any;
}

const FormSection = ({ title, fields, control }: FormSectionProps) => (
    <div className="space-y-4 border p-4 rounded">
        <h3 className="text-lg font-medium">{title}</h3>
        <div className="grid grid-cols-2 gap-4">
            {fields.map(({ name, label, type = "text" }) => (
                <FormField
                    key={name}
                    name={name}
                    control={control}
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>{label}</FormLabel>
                            <FormControl>
                                <Input
                                    type={type}
                                    {...field}
                                    onChange={e => field.onChange(
                                        type === "number" ? parseFloat(e.target.value) : e.target.value
                                    )}
                                />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
            ))}
        </div>
    </div>
);

const SatelliteForm: React.FC<SatelliteFormProps> = ({
    initialData,
    onRefresh,
    onClose,
}) => {
    const [dynamics, setDynamics] = useState<Dynamics[]>([]);

    useEffect(() => {
        const loadDynamics = async () => {
            try {
                const data = await fetchDynamics();
                setDynamics(data.items);
            } catch (error) {
                toast.error("Failed to load dynamics options.");
            }
        };
        loadDynamics();
    }, []);

    const form = useForm<SatelliteFormValues>({
        resolver: zodResolver(satelliteSchema),
        defaultValues: initialData || {
            name: "",
            group: "",
            dryMass: 0,
            dragArea: 0,
            dragCoefficient: 2.2,
            srpArea: 0,
            srpCoefficient: 1.8,
            tleConfig: {
                noradId: 0,
                classification: "U",
                launchYear: new Date().getFullYear(),
                launchNumber: 1,
                pieceOfLaunch: "A",
            },
            propulsion: {
                name: "",
                direction: "",
                isp: 0,
                thrustLevel: 0,
                minBurnDuration: 0,
                maxBurnDuration: 0,
            },
            aocs: {
                name: "",
                maximumAngVel: 0,
            },
            gnss: {
                name: "",
                posXStd: 0,
                posYStd: 0,
                posZStd: 0,
                velStd: 0,
            },
            dynamicsId: "",
        },
    });

    const onSubmit = async (data: SatelliteFormValues) => {
        try {
            await createOrUpdateSatellite({
                ...data,
                id: initialData?.id || "",
            });
            toast.success(
                `Satellite ${initialData ? "updated" : "created"} successfully!`
            );
            onRefresh();
            onClose();
        } catch (error) {
            toast.error("Error saving satellite. Please try again.");
        }
    };

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                <FormSection
                    title="Basic Information"
                    control={form.control}
                    fields={[
                        { name: "name", label: "Name" },
                        { name: "group", label: "Group" },
                        { name: "dryMass", label: "Dry Mass (kg)", type: "number" },
                    ]}
                />

                <FormSection
                    title="Drag Configuration"
                    control={form.control}
                    fields={[
                        { name: "dragArea", label: "Drag Area (m²)", type: "number" },
                        { name: "dragCoefficient", label: "Drag Coefficient", type: "number" },
                    ]}
                />

                <FormSection
                    title="SRP Configuration"
                    control={form.control}
                    fields={[
                        { name: "srpArea", label: "SRP Area (m²)", type: "number" },
                        { name: "srpCoefficient", label: "SRP Coefficient", type: "number" },
                    ]}
                />

                <FormSection
                    title="TLE Configuration"
                    control={form.control}
                    fields={[
                        { name: "tleConfig.noradId", label: "NORAD ID", type: "number" },
                        { name: "tleConfig.launchYear", label: "Launch Year", type: "number" },
                        { name: "tleConfig.launchNumber", label: "Launch Number", type: "number" },
                        { name: "tleConfig.pieceOfLaunch", label: "Piece of Launch" },
                    ]}
                />

                <FormSection
                    title="Propulsion System"
                    control={form.control}
                    fields={[
                        { name: "propulsion.name", label: "Name" },
                        { name: "propulsion.direction", label: "Direction" },
                        { name: "propulsion.isp", label: "ISP", type: "number" },
                        { name: "propulsion.thrustLevel", label: "Thrust Level", type: "number" },
                        { name: "propulsion.minBurnDuration", label: "Min Burn Duration", type: "number" },
                        { name: "propulsion.maxBurnDuration", label: "Max Burn Duration", type: "number" },
                    ]}
                />

                <FormSection
                    title="AOCS Configuration"
                    control={form.control}
                    fields={[
                        { name: "aocs.name", label: "AOCS Name" },
                        { name: "aocs.maximumAngVel", label: "Maximum Angular Velocity", type: "number" },
                    ]}
                />

                <FormSection
                    title="GNSS Configuration"
                    control={form.control}
                    fields={[
                        { name: "gnss.name", label: "GNSS Name" },
                        { name: "gnss.velStd", label: "Velocity STD", type: "number" },
                        { name: "gnss.posXStd", label: "Position X STD", type: "number" },
                        { name: "gnss.posYStd", label: "Position Y STD", type: "number" },
                        { name: "gnss.posZStd", label: "Position Z STD", type: "number" },
                    ]}
                />

                {/* Dynamics selection needs special handling due to Select component */}
                <FormField
                    name="dynamicsId"
                    control={form.control}
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Dynamics Configuration</FormLabel>
                            <Select
                                onValueChange={field.onChange}
                                defaultValue={field.value}
                            >
                                <FormControl>
                                    <SelectTrigger>
                                        <SelectValue placeholder="Select dynamics configuration" />
                                    </SelectTrigger>
                                </FormControl>
                                <SelectContent>
                                    {dynamics.map((dyn) => (
                                        <SelectItem key={dyn.id} value={dyn.id}>
                                            {dyn.name}
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                <div className="flex justify-end space-x-4">
                    <Button type="button" variant="outline" onClick={onClose}>
                        Cancel
                    </Button>
                    <Button type="submit">
                        {initialData ? "Update" : "Create"} Satellite
                    </Button>
                </div>
            </form>
        </Form>
    );
};

export default SatelliteForm;
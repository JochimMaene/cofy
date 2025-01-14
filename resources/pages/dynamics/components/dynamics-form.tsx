import React from "react";
import { useForm, SubmitHandler } from "react-hook-form";
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form";
import { toast } from "sonner";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Dynamics } from "@/types/dynamics";
import { createOrUpdateDynamics } from "@/services/dynamics";

interface DynamicsFormProps {
    initialData?: Dynamics; // Optional for updates
    onRefresh: () => void;
    onClose: () => void; // Close the dialog
}

interface DynamicsFormValues {
    name: string;
    harmonicsDegree: number;
    harmonicsOrder: number;
    solarRadiationPressure: boolean;
    drag: boolean;
    solidTides: boolean;
    thirdBodySun: boolean;
    thirdBodyMoon: boolean;
}

const DynamicsForm: React.FC<DynamicsFormProps> = ({
    initialData,
    onRefresh,
    onClose,
}) => {
    const form = useForm<DynamicsFormValues>({
        defaultValues: initialData || {
            name: "",
            harmonicsDegree: 0,
            harmonicsOrder: 0,
            solarRadiationPressure: false,
            drag: false,
            solidTides: false,
            thirdBodySun: false,
            thirdBodyMoon: false,
        },
    });

    const onSubmit: SubmitHandler<DynamicsFormValues> = async (data) => {
        const dynamicsData: Dynamics = {
            ...data,
            id: initialData?.id || "", // Include `id` if editing
        };
        try {
            await createOrUpdateDynamics(dynamicsData);
            toast.success(
                initialData ? "Dynamics updated successfully!" : "Dynamics created successfully!"
            );
            onRefresh(); // Trigger parent refresh
            onClose();   // Close dialog
        } catch (error) {
            toast.error("Error saving dynamics. Please try again.");
        }
    };

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                {/* Name Field */}
                <FormField
                    name="name"
                    control={form.control}
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Name</FormLabel>
                            <FormControl>
                                <Input
                                    type="text"
                                    placeholder="Enter a dynamics name"
                                    {...field}
                                    className="input"
                                />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                {/* Harmonics Degree Field */}
                <FormField
                    name="harmonicsDegree"
                    control={form.control}
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Harmonics Degree</FormLabel>
                            <FormControl>
                                <Input
                                    type="number"
                                    placeholder="Enter harmonics degree"
                                    {...field}
                                    className="input"
                                />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                {/* Harmonics Order Field */}
                <FormField
                    name="harmonicsOrder"
                    control={form.control}
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Harmonics Order</FormLabel>
                            <FormControl>
                                <Input
                                    type="number"
                                    placeholder="Enter harmonics order"
                                    {...field}
                                    className="input"
                                />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                {/* Checkboxes */}
                {[
                    { name: "solarRadiationPressure", label: "Solar Radiation Pressure" },
                    { name: "drag", label: "Drag" },
                    { name: "solidTides", label: "Solid Tides" },
                    { name: "thirdBodySun", label: "Third Body Sun" },
                    { name: "thirdBodyMoon", label: "Third Body Moon" },
                ].map((checkbox) => (
                    <FormField
                        key={checkbox.name}
                        name={checkbox.name as keyof DynamicsFormValues}
                        control={form.control}
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>{checkbox.label}</FormLabel>
                                <FormControl>
                                    <Checkbox
                                        checked={Boolean(field.value)} // Coerce to boolean
                                        onCheckedChange={(checked) => field.onChange(checked === true)}
                                        className="checkbox"
                                    />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                ))}
                {/* Submit Button */}
                <Button
                    type="submit"
                    variant="default"
                    size="default"
                    className="w-full"
                >

                    {initialData ? "Update Dynamics" : "Create Dynamics"}
                </Button>
            </form>
        </Form>
    );
};

export default DynamicsForm;

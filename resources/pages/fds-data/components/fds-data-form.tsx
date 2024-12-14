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
import { Input } from "@/components/ui/input";
import { FdsData } from "@/types/fds-data";
import { Button } from "@/components/ui/button";

import { updateFdsData } from "@/services/fds-data";

interface FdsDataFormProps {
    initialData: FdsData;
    onRefresh: () => void;
    onClose: () => void; // Close the dialog
}

interface FdsDataFormValues {
    cron: string;
    URL: string;
}

const FdsDataForm: React.FC<FdsDataFormProps> = ({
    initialData,
    onRefresh,
    onClose,
}) => {
    const form = useForm<FdsDataFormValues>({
        defaultValues: initialData
    });


    const onSubmit: SubmitHandler<FdsDataFormValues> = async (data) => {
        const fdsData: FdsData = {
            ...data,
            id: initialData?.id,
            name: initialData?.name,
            lastUpdate: initialData?.lastUpdate,
            nextUpdate: initialData?.nextUpdate,
            status: initialData?.status,
        };
        try {
            await updateFdsData(fdsData);
            toast.success(
                "Fds data updated successfully!"
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
                {/* Harmonics Degree Field */}
                <FormField
                    name="cron"
                    control={form.control}
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Cron expression</FormLabel>
                            <FormControl>
                                <Input
                                    type="string"
                                    placeholder="Enter cron"
                                    {...field}
                                    className="input"
                                />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                {/* Data source URL */}
                <FormField
                    name="URL"
                    control={form.control}
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Data source URL</FormLabel>
                            <FormControl>
                                <Input
                                    type="string"
                                    placeholder="Enter Url"
                                    {...field}
                                    className="input"
                                />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                {/* Submit Button */}
                <Button
                    type="submit"
                    variant="default"
                    size="default"
                    className="w-full"
                >

                    Update FDS Data settings
                </Button>

            </form>
        </Form>
    );
};

export default FdsDataForm;

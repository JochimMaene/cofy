import { Satellite } from "@/types/satellite";
import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";

interface SatelliteDetailsProps {
    satellite: Satellite;
}

const SatelliteDetails: React.FC<SatelliteDetailsProps> = ({ satellite }) => {
    return (
        <div className="grid grid-cols-2 gap-4">
            <Card>
                <CardHeader>
                    <CardTitle>Basic Information</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                    <div><strong>Name:</strong> {satellite.name}</div>
                    <div><strong>Group:</strong> {satellite.group || '-'}</div>
                    <div><strong>Dry Mass:</strong> {satellite.dryMass} kg</div>
                    <div><strong>Drag Area:</strong> {satellite.dragArea} m²</div>
                    <div><strong>Drag Coefficient:</strong> {satellite.dragCoefficient}</div>
                    <div><strong>SRP Area:</strong> {satellite.srpArea} m²</div>
                    <div><strong>SRP Coefficient:</strong> {satellite.srpCoefficient}</div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle>TLE Configuration</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                    <div><strong>NORAD ID:</strong> {satellite.tleConfig.noradId}</div>
                    <div><strong>Classification:</strong> {satellite.tleConfig.classification}</div>
                    <div><strong>Launch Year:</strong> {satellite.tleConfig.launchYear}</div>
                    <div><strong>Launch Number:</strong> {satellite.tleConfig.launchNumber}</div>
                    <div><strong>Piece of Launch:</strong> {satellite.tleConfig.pieceOfLaunch}</div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle>Propulsion System</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                    <div><strong>Name:</strong> {satellite.propulsion.name}</div>
                    <div><strong>Direction:</strong> {satellite.propulsion.direction}</div>
                    <div><strong>ISP:</strong> {satellite.propulsion.isp}</div>
                    <div><strong>Thrust Level:</strong> {satellite.propulsion.thrustLevel}</div>
                    <div><strong>Min Burn Duration:</strong> {satellite.propulsion.minBurnDuration}</div>
                    <div><strong>Max Burn Duration:</strong> {satellite.propulsion.maxBurnDuration}</div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle>AOCS & GNSS</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="space-y-4">
                        <div>
                            <h4 className="font-semibold mb-2">AOCS</h4>
                            <div><strong>Name:</strong> {satellite.aocs.name}</div>
                            <div><strong>Maximum Angular Velocity:</strong> {satellite.aocs.maximumAngVel}</div>
                        </div>
                        <div>
                            <h4 className="font-semibold mb-2">GNSS</h4>
                            <div><strong>Name:</strong> {satellite.gnss.name}</div>
                            <div><strong>Position STD:</strong> X: {satellite.gnss.posXStd}, Y: {satellite.gnss.posYStd}, Z: {satellite.gnss.posZStd}</div>
                            <div><strong>Velocity STD:</strong> {satellite.gnss.velStd}</div>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
};

export default SatelliteDetails;
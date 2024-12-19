const Home: React.FC = () => {
  return (
    <div className="flex flex-col gap-4">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      {/* Add your dashboard components here */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {/* Example placeholder for future dashboard cards */}
        <div className="rounded-lg border p-4">
          <h2 className="font-semibold">Satellites Overview</h2>
          <p className="text-muted-foreground">Coming soon...</p>
        </div>
        <div className="rounded-lg border p-4">
          <h2 className="font-semibold">Dynamics Status</h2>
          <p className="text-muted-foreground">Coming soon...</p>
        </div>
        <div className="rounded-lg border p-4">
          <h2 className="font-semibold">FDS Data Status</h2>
          <p className="text-muted-foreground">Coming soon...</p>
        </div>
        <div className="rounded-lg border p-4">
          <h2 className="font-semibold">System Health</h2>
          <p className="text-muted-foreground">Coming soon...</p>
        </div>
      </div>
    </div>
  );
};

export default Home;

using UnityEngine;
using System.Collections.Generic;
using Zeptomoby.OrbitTools;
using System;
public class satelliteManagerV2 : MonoBehaviour
{
    [SerializeField] private float minCollisionRadiusKm = 6500f;
    [SerializeField] private float maxCollisionRadiusKm = 30000f;

    private readonly List<typeSatellite> collisionSats = new List<typeSatellite>();
    public List<typeSatellite> CollisionSatellites => collisionSats;


    private readonly List<typeSatellite> sats = new List<typeSatellite>();
    public List<typeSatellite> Satellites => sats;

    public inputHandling inputHandler;
    private float dt;
    private DateTime currentTime;
    public DateTime CurrentTime => currentTime;
    private float satDensity = 470.1002078863646f;
    float scale = simulationConstants.scaleFactor;
    void Start()
    {
        currentTime = DateTime.UtcNow;
    }
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.T))
        {
            ToggleCovarianceShapes();   
        }
    }
    // 50Hz update rate
    void FixedUpdate()
    {
        dt = Time.fixedDeltaTime * inputHandler.timeScale; // fixed scaled timestep
        currentTime = currentTime.AddSeconds(dt);

        for (int i = 0; i < sats.Count; i++)
        {
            var sat = sats[i];

            if (sat == null || sat.sgp4Satellite == null) {Debug.LogWarning(sat.name); continue;}
           
            try
            {
                Eci eci = sat.sgp4Satellite.PositionEci(currentTime);
                Vector3 positionKm = new Vector3(
                        (float)eci.Position.Y,
                        (float)eci.Position.Z,
                        (float)eci.Position.X
                    );

                Vector3 velocityKmS  = new Vector3(
                        (float)eci.Velocity.Y,
                        (float)eci.Velocity.Z,
                        (float)eci.Velocity.X
                    );

                sat.posKm = positionKm;
                sat.velKmS = velocityKmS;

                sat.transform.position = positionKm * scale;
                sat.velocity = velocityKmS * scale;
            }
            catch
            {
                Debug.LogWarning($"Prop failed for {sat.name}");
                Destroy(sat.gameObject);
                collisionSats.Remove(sat);
                sats.RemoveAt(i);
                i--;
            }
        }
    }
    public void AssignSatRadii(string data)
    {
        float mass;
        float totalMass=0;
        float avgMass;
        int count=0;

        string [] rawLines = data.Split(new[] {'\r', '\n'}, StringSplitOptions.RemoveEmptyEntries);
        
        // Currently assumes sat mass data will be in the same order as TLE sat data. (Need to check if actually true)
        for (int i = 0; i < sats.Count; i++)
        {
            try
            {
            mass = ExtractMass(rawLines[3*i+3]);
            sats[i].mass = mass;
            if (mass != -1)
            {
                totalMass += mass;
                count += 1;
            }
            }
            catch{continue;}
        }
        avgMass = totalMass/count;
        for (int i = 0; i < sats.Count; i++)
        {
            if (sats[i].mass == -1)
            {
                sats[i].mass = avgMass;
            }
        }

        for (int i = 0; i < sats.Count; i++)
        {
            sats[i].radius = Mass2Radius(sats[i].mass);
        }
        
    }
    private float ExtractMass(string massLine)
    {
        float mass;
        mass = float.Parse(massLine);
        return mass;
    }
    private float Mass2Radius(float mass)
    {
        float radius = (float)Math.Pow((3f * mass) / (4f * (float)Math.PI * satDensity), 1f / 3f);
        return radius;
    }
    public void Register(typeSatellite sat)
    {
        sats.Add(sat);

        if (IsInCollisionRegion(sat))
        {
            collisionSats.Add(sat);
        }
    }

    public string[][] ReadCSV(string SatCovData)
    {
        string[] lines = SatCovData.Split("\n");

        List<string[]> CovArray = new List<string[]>();

        foreach (string line in lines)
        {
            string[] row = line.Split(",");
            CovArray.Add(row);
        }

        return CovArray.ToArray();
    }
    public void AssignSatCov(string[] names, string[][] CovData)
    {
        // Get position of each satellite in the CSV covariance data file
        foreach (typeSatellite sat in sats)
        {
            int index = Array.IndexOf(names, sat.name);

            if (index<0) continue; // Skip if sat not found

            // Therefore, assign covariance values to sat
            for (int i = 0; i < 6; i++)
            {
                for (int j = 0; j < 6; j++)
                {
                    int flatIndex = 2 + (i * 6 + j);
                    float.TryParse(CovData[index][flatIndex], out sat.CovMatrix[i, j]);                }
            }
            //Debug.Log(sat.name);
        }
    }
    private bool IsInCollisionRegion(typeSatellite sat)
    {
        if (sat == null || sat.sgp4Satellite == null)
            return false;

        try
        {
            Eci eci = sat.sgp4Satellite.PositionEci(DateTime.UtcNow);

            Vector3 posKm = new Vector3(
                (float)eci.Position.Y,
                (float)eci.Position.Z,
                (float)eci.Position.X
            );

            float orbitalRadiusKm = posKm.magnitude;

            return orbitalRadiusKm >= minCollisionRadiusKm &&
            orbitalRadiusKm <= maxCollisionRadiusKm;
        }
        catch
        {
            return false;
        }
    }

    private bool showCovarianceShapes = false;

    public void ToggleCovarianceShapes()
    {
        showCovarianceShapes = !showCovarianceShapes;

        foreach (typeSatellite sat in sats)
        {
            sat.showCovarianceShape = showCovarianceShapes;
        }
    }
}
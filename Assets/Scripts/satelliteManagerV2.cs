using UnityEngine;
using System.Collections.Generic;
using Zeptomoby.OrbitTools;
using System;
public class satelliteManagerV2 : MonoBehaviour
{
    private readonly List<typeSatellite> sats = new List<typeSatellite>();
    public inputHandling inputHandler;
    private float dt;
    private DateTime currentTime;
    private float satDensity = 858.1138838346274f;
    float scale = simulationConstants.scaleFactor;
    void Start()
    {
        currentTime = DateTime.UtcNow;
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
           
            try{
            Eci eci = sat.sgp4Satellite.PositionEci(currentTime);
            Vector3 position = new Vector3(
                    (float)eci.Position.Y,
                    (float)eci.Position.Z,
                    (float)eci.Position.X
                ) * scale;

            sat.transform.position = position;

            Vector3 velocity  = new Vector3(
                    (float)eci.Velocity.Y,
                    (float)eci.Velocity.Z,
                    (float)eci.Velocity.X
                ) * scale;

            sat.velocity = velocity;
            }
            catch{
                Debug.LogWarning("Prop failed for {sat.name}");
                Destroy(sat);
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
    public void Register(satelliteMotionV5 sat)
    {
        sats.Add(sat);
    }
}
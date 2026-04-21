using System;
using System.Globalization;
using UnityEngine;

public class satelliteSpawner : MonoBehaviour
{
    [Header("Satellite Spawner Settings")]
    [SerializeField] private TextAsset TLEData;
    [SerializeField] private GameObject satellitePrefab;
    [SerializeField] private satelliteManagerV2 manager;
    [SerializeField] private TextAsset MassData;
    [SerializeField] private TextAsset SatCovData;
    
    private string[][] CovData;
    string[] CovNames;
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Awake()
    {
        LoadSatsFromTLE(TLEData.text);
        CovData = manager.ReadCSV(SatCovData.text);
    }
    void Start()
    {
        manager.AssignSatRadii(MassData.text);
        CovNames = GetNames(CovData);
        manager.AssignSatCov(CovNames, CovData);
    }

    private void LoadSatsFromTLE(string tleData)
    {
        string [] rawLines = tleData.Split(new[] {'\r', '\n'}, StringSplitOptions.RemoveEmptyEntries);

        // For each TLE sat
        for (int i = 0; i + 2 < rawLines.Length; i += 3)
        {
            string name = rawLines[i].Trim();
            string line1 = rawLines[i + 1].Trim();
            string line2 = rawLines[i + 2].Trim();

            GameObject satellite = Instantiate(satellitePrefab, Vector3.zero, Quaternion.identity);
            satellite.name = name;

            typeSatellite orbit = satellite.GetComponent<typeSatellite>();
            if (orbit == null)
            {
                Debug.LogError($"Orbit missing for {name}");
                Destroy(satellite);
                continue;
            }

            try
            {
                orbit.IntialiseOrbit(name, line1, line2);
                manager.Register(orbit);
            }
            catch (Exception)
            {
                Debug.LogWarning($"Failed to load TLE for {orbit.name}");
                Destroy(satellite);
            }
        }
    }
    private string[] GetNames(string[][] CovData)
    {
        int height = CovData.Length;
        string[] names = new string[height];

        for (int i=1; i<height; i++)
        {
            names[i] = CovData[i][0];
        }
        return names;
    }
}

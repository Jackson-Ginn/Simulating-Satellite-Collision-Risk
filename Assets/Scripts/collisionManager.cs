using UnityEngine;
using System.Collections.Generic;
using System.IO;
using System.Text;

// Find satellites which are close enough to analyse collision probability

public class collisionManager : MonoBehaviour
{
    // --- Data saving
    [SerializeField] private bool exportCandidatePairs = true;
    private string exportPath;
    private bool hasWrittenHeader = false;
    // --- End

    [SerializeField] private satelliteManagerV2 satManager;

    [SerializeField] private float screeningIntervalSeconds = 5f;
    // If two sats are close than xx km they are stored
    [SerializeField] private float screeningDistanceKm = 20f;
    // Spatial grid size
    [SerializeField] private float gridSizeKm = 50f;
    private float timer;


    // Stores the pair of satellites as their position in the list of sats
    public struct SatPair
    {
        public int A;
        public int B;

        public SatPair(int a, int b)
        {
            A = a;
            B = b;
        }
    }

    // For finding neighbouring cells (only forward to stop double counting)
    // This is cell index offset not physical distance, physical size is unpacked
    private static readonly Vector3Int[] ForwardNeighbourOffsets =
    {
        // Axis aligned
        new Vector3Int(1, 0, 0),
        new Vector3Int(0, 1, 0),
        new Vector3Int(0, 0, 1),

        // 2D diagonals
        new Vector3Int(1, 1, 0),
        new Vector3Int(1, -1, 0),
        new Vector3Int(1, 0, 1),
        new Vector3Int(1, 0, -1),
        new Vector3Int(0, 1, 1),
        new Vector3Int(0, 1, -1),

        // 3D diagonals
        new Vector3Int(1, 1, 1),
        new Vector3Int(1, 1, -1),
        new Vector3Int(1, -1, 1),
        new Vector3Int(1, -1, -1)
    };

    // Initalise export path
    void Start()
    {
        exportPath = Path.Combine(Application.persistentDataPath, "cadidate_pairs.csv");
        Debug.Log($"Cadidate pair export path: {exportPath}");
    }
    // Update is called once per frame
    void Update()
    {
        timer += Time.deltaTime;

        // Sat propagation is continuous but detection only periodic to reduce compuational cost
        if (timer >= screeningIntervalSeconds)
        {
            timer = 0f;
            Screening();   
        }
    }

    private void Screening()
    {
        // Gets list of active sats from sat manager (which are not beyond screening altitude)
        List<typeSatellite> sats = satManager.CollisionSatellites;

        // Creates spatial grid (Vector3Int stores grid cell coordinate, List stores indices of sats inside each grid cell)
        Dictionary<Vector3Int, List<int>> grid = new Dictionary<Vector3Int, List<int>>();
        // So this dict stores a vector3 of the grid cell and a list of satellite indexes which are in said cell

        // Coverts current sat position into a grid cell
        for (int i = 0; i < sats.Count; i++)
        {
            // Skip satellites that have not yet been propagated
            if (sats[i].posKm == Vector3.zero) continue;

            // Find cell which sat belongs in
            Vector3Int cell = Pos2Cell(sats[i].posKm);

            // Create cell if not already a sat inside
            if (!grid.ContainsKey(cell))
                grid[cell] = new List<int>();

            // Add sat to cell
            grid[cell].Add(i);
        }

        // Pairs within cells and neighbouring cells which are close enough get logged into cadidatePairs
        List<SatPair> candidatePairs = new List<SatPair>();

        foreach (var entry in grid)
        {
            Vector3Int cell = entry.Key;
            List<int> satsInCell = entry.Value;

            // Check pairs inside the same cell
            CheckPairsInCell(satsInCell, sats, candidatePairs);

            // Check pairs between this cell and selected neighbouring cells
            foreach (Vector3Int offset in ForwardNeighbourOffsets)
            {
                Vector3Int neighbourCell = cell + offset;

                if (grid.TryGetValue(neighbourCell, out List<int> neighbourSats))
                {
                    CheckPairsBetweenCells(satsInCell, neighbourSats, sats, candidatePairs);
                }
            }
        }

        Debug.Log($"Candidate pairs found: {candidatePairs.Count}");

        //if (candidatePairs.Count > 0)
        //{
        //    foreach (SatPair pair in candidatePairs)
        //    {
        //        Debug.Log(
        //            $"{sats[pair.A].name} - {sats[pair.B].name}, " +
        //            $"distance = {(sats[pair.A].posKm - sats[pair.B].posKm).magnitude} km, " +
        //            $"posA = {sats[pair.A].posKm}, posB = {sats[pair.B].posKm}"
        //        );
        //    }
        //}


        // EXPORT DATA
        ExportCandidatePairs(candidatePairs, sats);
        Debug.Log($"Candidate pairs found: {candidatePairs.Count}");

    }

    // Putting a sat in a grid cell based on position and grid size
    private Vector3Int Pos2Cell(Vector3 posKm)
    {
        return new Vector3Int(
            Mathf.FloorToInt(posKm.x/gridSizeKm),
            Mathf.FloorToInt(posKm.y/gridSizeKm),
            Mathf.FloorToInt(posKm.z/gridSizeKm)
        );
    }

    private void CheckPairsInCell(List<int> indices, List<typeSatellite> sats, List<SatPair> candidatePairs)
    {
        for (int i = 0; i < indices.Count; i++)
        {
            for (int j = i+1; j < indices.Count; j++)
            {
                int a = indices[i];
                int b = indices[j];

                float distanceKm = Vector3.Distance(sats[a].posKm, sats[b].posKm);

                if (distanceKm < screeningDistanceKm)
                {
                    candidatePairs.Add(new SatPair(a,b));
                }
            }
        }
    }
    private void CheckPairsBetweenCells(
        List<int> cellA,
        List<int> cellB,
        List<typeSatellite> sats,
        List<SatPair> candidatePairs)
    {
        for (int i = 0; i < cellA.Count; i++)
        {
            for (int j = 0; j < cellB.Count; j++)
            {
                int a = cellA[i];
                int b = cellB[j];

                float distanceKm = Vector3.Distance(
                    sats[a].posKm,
                    sats[b].posKm
                );

                if (distanceKm < screeningDistanceKm)
                {
                    candidatePairs.Add(new SatPair(a, b));
                }
            }
        }
    }


    // DATA EXPORTING
    private void ExportCandidatePairs(
    List<SatPair> candidatePairs,
    List<typeSatellite> sats)
    {
        if (!exportCandidatePairs || candidatePairs.Count == 0)
            return;

        StringBuilder sb = new StringBuilder();

        if (!hasWrittenHeader)
        {
            sb.AppendLine(
                "simTime," +
                "satA,satB," +
                "satA_x_km,satA_y_km,satA_z_km," +
                "satB_x_km,satB_y_km,satB_z_km," +
                "distance_km," +
                "satA_vx_km_s,satA_vy_km_s,satA_vz_km_s," +
                "satB_vx_km_s,satB_vy_km_s,satB_vz_km_s," +
                "relative_speed_km_s"
            );

            hasWrittenHeader = true;
        }

        foreach (SatPair pair in candidatePairs)
        {
            typeSatellite satA = sats[pair.A];
            typeSatellite satB = sats[pair.B];

            Vector3 relPos = satA.posKm - satB.posKm;
            Vector3 relVel = satA.velKmS - satB.velKmS;

            float distanceKm = relPos.magnitude;
            float relativeSpeedKmS = relVel.magnitude;

            sb.AppendLine(
                $"{satManager.CurrentTime.ToString("o")}," +
                $"{satA.name},{satB.name}," +
                $"{satA.posKm.x},{satA.posKm.y},{satA.posKm.z}," +
                $"{satB.posKm.x},{satB.posKm.y},{satB.posKm.z}," +
                $"{distanceKm}," +
                $"{satA.velKmS.x},{satA.velKmS.y},{satA.velKmS.z}," +
                $"{satB.velKmS.x},{satB.velKmS.y},{satB.velKmS.z}," +
                $"{relativeSpeedKmS}"
            );
        }

        File.AppendAllText(exportPath, sb.ToString());
    }
}

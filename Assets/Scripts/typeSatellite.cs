using UnityEngine;
using Zeptomoby.OrbitTools;
public class typeSatellite : MonoBehaviour
{
    [Header("Fetched Orbit Parameters")]
    public Vector3 posKm;
    public Vector3 velKmS;
    public Vector3 velocity;
    public string name;
    public string tleLine1;
    public string tleLine2;
    public float mass;
    public float radius;
    public float[,] CovMatrix = new float[6,6];
    public Satellite sgp4Satellite;

    [Header("Visual Shape")]
    public Transform visualModel;
    public Vector3 defaultShape = Vector3.one;
    public Vector3 satShape = Vector3.one;
    public bool showCovarianceShape = false;
    public float covarianceScaleFactor = 1f;

    void Start()
    {
        if (visualModel == null)
            visualModel = transform;
        defaultShape = visualModel.localScale;
    }

    void Update()
    {
        if (visualModel == null)
            return;

        if (showCovarianceShape)
            ApplyCovarianceShape();
        else
            visualModel.localScale = defaultShape;
    }

    public void IntialiseOrbit(string satName, string line1, string line2)
    {
        name = satName;
        tleLine1 = line1;
        tleLine2 = line2;

        Tle tle = new Tle(satName, line1, line2);
        sgp4Satellite = new Satellite(tle);
    }

    void ApplyCovarianceShape()
    {
        if (CovMatrix == null || visualModel == null)
            return;

        float radial = Mathf.Sqrt(Mathf.Abs(CovMatrix[0, 0]));
        float inTrack = Mathf.Sqrt(Mathf.Abs(CovMatrix[1, 1]));
        float crossTrack = Mathf.Sqrt(Mathf.Abs(CovMatrix[2, 2]));

        satShape = new Vector3(radial, crossTrack, inTrack) * covarianceScaleFactor;

        visualModel.localScale = satShape;

        ApplyRICOrientation();
    }

    void ApplyRICOrientation()
    {
        if (posKm == Vector3.zero || velKmS == Vector3.zero)
            return;

        Vector3 radialDir = posKm.normalized;
        Vector3 crossTrackDir = Vector3.Cross(posKm, velKmS).normalized;
        Vector3 inTrackDir = Vector3.Cross(crossTrackDir, radialDir).normalized;

        visualModel.rotation = Quaternion.LookRotation(inTrackDir, crossTrackDir);
    }

}
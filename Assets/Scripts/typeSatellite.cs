using UnityEngine;
using Zeptomoby.OrbitTools;
public class typeSatellite : MonoBehaviour
{
    [Header("Fetched Orbit Parameters")]
    public Vector3 velocity;
    public string name;
    public string tleLine1;
    public string tleLine2;
    public float mass;
    public float radius;
    public float[,] CovMatrix = new float[6,6];
    public Satellite sgp4Satellite;
    public void IntialiseOrbit(string satName, string line1, string line2)
    {
        name = satName;
        tleLine1 = line1;
        tleLine2 = line2;

        Tle tle = new Tle(satName, line1, line2);
        sgp4Satellite = new Satellite(tle);
    }
}

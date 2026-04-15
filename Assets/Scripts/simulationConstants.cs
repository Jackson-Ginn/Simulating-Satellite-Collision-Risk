using UnityEngine;

public class simulationConstants
{
    // gravitational constant
    public const double gravitationalConstant = 6.67430e-11; // m^3 kg^-1 s^-2

    // mass of Earth constant
    public const double earthMass = 5.972e24; // in SI kg

    // earth diameter constant
    public const double earthDiameter = 12756; // in SI km

    // earth radius constant
    public const double earthRadius = earthDiameter / 2.0; // in SI km

    // scale factor constant
    public const float scaleFactor = 1.0f / 100.0f; // 100 km to 1 Unity unit SI -> Uu
}
using UnityEngine;

public class earthScale : MonoBehaviour
{
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Awake()
    {
        float scaleDiameter = (float)simulationConstants.earthDiameter * (float)simulationConstants.scaleFactor / 2;
        transform.localScale = new Vector3(scaleDiameter, scaleDiameter, scaleDiameter);
    }
    
}

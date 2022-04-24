using System.Diagnostics;

namespace dotnet_api_example.Utils;

public class ActivityUtil
{
    public static readonly ActivitySource Activity = new(nameof(ActivityUtil));
}

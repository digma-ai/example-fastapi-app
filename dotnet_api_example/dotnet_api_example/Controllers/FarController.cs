using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using dotnet_api_example.Utils;

namespace dotnet_api_example.Controllers;

[ApiController]
[Route("[controller]")]
public class FarController : ControllerBase
{
    public FarController()
    {
    }

    [HttpGet(Name = "far")]
    public string Get()
    {
        using (var activity = ActivityUtil.Activity.StartActivity("Far Route", ActivityKind.Producer)) {
            return "FAR OUT!!!";
        }
    }
}

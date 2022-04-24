using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;

namespace dotnet_api_example.Controllers;

[ApiController]
[Route("[controller]")]
public class SuccessController : ControllerBase
{
    private static readonly ActivitySource Activity = new("SuccessController");

    public SuccessController()
    {
    }

    [HttpGet(Name = "success")]
    public string Get()
    {
        using (var activity = Activity.StartActivity("Working Endpoint", ActivityKind.Producer)) {
            return "This endpoint works. Hurray!";
        }
    }
}

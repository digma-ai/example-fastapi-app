using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;

namespace dotnet_api_example.Controllers;

[ApiController]
[Route("[controller]")]
public class TransferController : ControllerBase
{
    private static readonly ActivitySource Activity = new(nameof(TransferController));



    private readonly ILogger<TransferController> _logger;

    public TransferController(ILogger<TransferController> logger)
    {
        _logger = logger;
    }

    [HttpGet(Name = "deposit")]
    public IEnumerable<TransferResult> Get()
    {
        using (var activity = Activity.StartActivity("Injest OTEL Data", ActivityKind.Producer)){
            throw new Exception("Blah");

        }

    }
}


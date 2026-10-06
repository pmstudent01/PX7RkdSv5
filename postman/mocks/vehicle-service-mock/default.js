const http = require("http");

const server = http.createServer((req, res) => {
  const method = req.method;
  const url = req.url.split("?")[0];

  // Match /vehicles/:id pattern
  const vehicleIdMatch = url.match(/^\/vehicles\/([^/]+)$/);

  // POST /vehicles
  // @endpoint POST /vehicles
  if (method === "POST" && url === "/vehicles") {
    let body = "";
    req.on("data", chunk => { body += chunk; });
    req.on("end", () => {
      let parsed = {};
      try { parsed = JSON.parse(body); } catch (e) {}

      if (!parsed.vin) {
        res.writeHead(400, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ message: "Request body missing required attribute: vin" }));
        return;
      }

      res.writeHead(201, { "Content-Type": "application/json" });
      res.end(JSON.stringify({
        id: 1,
        nickName: parsed.nickName || "The Lisa Marie",
        vin: parsed.vin || "4M2DV11W4RDJ53329",
        make: parsed.make || "Mercury",
        model: parsed.model || "Villager",
        year: parsed.year || "1994",
        miles: parsed.miles ? parsed.miles.toLocaleString() : "159,864"
      }));
    });
    return;
  }

  // GET /vehicles/:id
  // @endpoint GET /vehicles/:id
  if (method === "GET" && vehicleIdMatch) {
    const id = vehicleIdMatch[1];

    if (id === "0") {
      res.writeHead(404, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ message: `Vehicle with id: ${id} not found.` }));
      return;
    }

    if (id === "99") {
      res.writeHead(500, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ message: "An unexpected error occurred." }));
      return;
    }

    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify([
      {
        id: 1,
        nickName: "The Lisa Marie",
        vin: "4M2DV11W4RDJ53329",
        make: "Mercury",
        model: "Villager",
        year: "1994",
        miles: 159864
      },
      {
        id: 2,
        nickName: "Dolly",
        vin: "JN8AZ2KR1AT169594",
        make: "Nissan",
        model: "Cube",
        year: "2010",
        miles: 59000
      }
    ]));
    return;
  }

  // PATCH /vehicles/:id
  // @endpoint PATCH /vehicles/:id
  if (method === "PATCH" && vehicleIdMatch) {
    const id = vehicleIdMatch[1];
    let body = "";
    req.on("data", chunk => { body += chunk; });
    req.on("end", () => {
      let parsed = {};
      try { parsed = JSON.parse(body); } catch (e) {}

      if (id === "99") {
        res.writeHead(500, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ message: "An unexpected error occurred." }));
        return;
      }

      if (!parsed || Object.keys(parsed).length === 0) {
        res.writeHead(400, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ message: "Bad request body." }));
        return;
      }

      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({
        id: parseInt(id) || 1,
        nickName: parsed.nickName || "The Lisa Marie",
        vin: parsed.vin || "4M2DV11W4RDJ53329",
        make: parsed.make || "Mercury",
        model: parsed.model || "Villager",
        year: parsed.year || "1994",
        miles: parsed.miles || 159999
      }));
    });
    return;
  }

  // DELETE /vehicles/:id
  // @endpoint DELETE /vehicles/:id
  if (method === "DELETE" && vehicleIdMatch) {
    const id = vehicleIdMatch[1];

    if (id === "99") {
      res.writeHead(500, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ message: "An unexpected error occurred." }));
      return;
    }

    res.writeHead(204);
    res.end("");
    return;
  }

  // 404 fallback
  res.writeHead(404, { "Content-Type": "application/json" });
  res.end(JSON.stringify({ message: "Route not found." }));
});

server.listen(process.env.PORT || 4500);

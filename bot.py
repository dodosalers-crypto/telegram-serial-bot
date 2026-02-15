export default {
  async fetch(request, env) {

    const url = new URL(request.url);

    // 🔒 SWITCH — change to true to enable registration
    const REGISTRATION_ENABLED = false;

    /* ================= API REGISTER ================= */
    if (url.pathname === "/api/register") {

      // 🔴 If disabled
      if (!REGISTRATION_ENABLED) {
        return new Response(
          JSON.stringify({
            success: false,
            message: "API DOWN"
          }),
          { headers: { "Content-Type": "application/json" } }
        );
      }

      try {
        const body = await request.json();
        const serial = body.serial?.trim();

        if (!serial) {
          return new Response(
            JSON.stringify({
              success: false,
              message: "NO SERIAL"
            }),
            { headers: { "Content-Type": "application/json" } }
          );
        }

        // check if already exists
        const exists = await env.LICENSE_DB.get(serial);

        if (exists) {
          return new Response(
            JSON.stringify({
              success: true,
              message: "ALREADY REGISTERED"
            }),
            { headers: { "Content-Type": "application/json" } }
          );
        }

        // save serial with value 1
        await env.LICENSE_DB.put(serial, "1");

        return new Response(
          JSON.stringify({
            success: true,
            message: "REGISTERED"
          }),
          { headers: { "Content-Type": "application/json" } }
        );

      } catch (e) {
        return new Response(
          JSON.stringify({
            success: false,
            message: "ERROR"
          }),
          { headers: { "Content-Type": "application/json" } }
        );
      }
    }

    /* ================= API CHECK (Tool ke liye) ================= */
    if (url.pathname === "/api/check") {

      const serial = url.searchParams.get("serial");

      if (!serial) {
        return new Response(
          JSON.stringify({ registered: false }),
          { headers: { "Content-Type": "application/json" } }
        );
      }

      const exists = await env.LICENSE_DB.get(serial);

      return new Response(
        JSON.stringify({
          registered: exists ? true : false
        }),
        { headers: { "Content-Type": "application/json" } }
      );
    }

    return new Response("API RUNNING");
  }
};

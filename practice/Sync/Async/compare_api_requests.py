"""Compare 100 real HTTP requests without relying on a public API.

Run: python practice/Sync/Async/compare_api_requests.py
Needs aiohttp (already available in the terminal Python used to test this).
The local API runs in a separate process and is stopped when the demo exits.
"""

import argparse
import asyncio
from concurrent.futures import ThreadPoolExecutor
import json
import multiprocessing
import os
import socket
import threading
import time
from urllib.request import ProxyHandler, build_opener

import aiohttp
from aiohttp import web


def serve_api(connection, delay):
    """One local API with product resources /products/1 through /products/N."""
    async def run():
        async def product(request):
            # Simulate an API waiting for its database, without blocking its loop.
            await asyncio.sleep(delay)
            response = web.json_response({
                "product_id": int(request.match_info["product_id"]),
                "source": "local training API",
            })
            # All client modes open a fresh connection for each request.
            response.force_close()
            return response

        app = web.Application()
        app.router.add_get("/products/{product_id:[0-9]+}", product)
        runner = web.AppRunner(app, access_log=None)
        await runner.setup()
        listener = socket.socket()
        listener.bind(("127.0.0.1", 0))
        listener.listen(256)
        site = web.SockSite(runner, listener)
        try:
            await site.start()
            connection.send(listener.getsockname()[1])
            connection.close()
            await asyncio.Event().wait()
        finally:
            await runner.cleanup()

    asyncio.run(run())


def compare(base_url, count, mode):
    observed_threads = set()
    lock = threading.Lock()
    thread_ready = None
    worker_state = threading.local()

    def record_thread():
        with lock:
            observed_threads.add(threading.get_native_id())

    def fetch(product_id):
        record_thread()
        if thread_ready is not None and not getattr(worker_state, "started", False):
            worker_state.started = True
            thread_ready.wait()
        # Ignore corporate/environment proxies for this loopback-only exercise.
        opener = build_opener(ProxyHandler({}))
        with opener.open(f"{base_url}/products/{product_id}", timeout=30) as response:
            return json.load(response)

    async def fetch_async(limit):
        connector = aiohttp.TCPConnector(limit=limit, force_close=True)
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            async def one(product_id):
                record_thread()
                async with session.get(f"{base_url}/products/{product_id}") as response:
                    response.raise_for_status()
                    return await response.json()

            # Tasks can wait for a free connection; limit controls active connections.
            return await asyncio.gather(*(one(i) for i in range(1, count + 1)))

    print(f"Starting {mode} (client PID {os.getpid()})...", flush=True)
    started = time.perf_counter()
    if mode == "sequential":
        results = [fetch(i) for i in range(1, count + 1)]
    elif mode.startswith("threads"):
        limit = int(mode.removeprefix("threads"))
        workers = min(limit, count)
        # For this experiment, wait until every worker has started before fetching.
        # Otherwise a fast response can finish before the pool creates all workers.
        thread_ready = threading.Barrier(workers, timeout=30)
        with ThreadPoolExecutor(max_workers=workers) as pool:
            results = list(pool.map(fetch, range(1, count + 1)))
    else:
        limit = int(mode.removeprefix("async"))
        results = asyncio.run(fetch_async(limit))
    seconds = time.perf_counter() - started

    # Verify responses, rather than treating a completed run as successful work.
    expected_ids = list(range(1, count + 1))
    if [r["product_id"] for r in results] != expected_ids:
        raise RuntimeError("Missing, duplicated or incorrect product responses")
    print(f"{mode:<14} {len(results):>9} {seconds:>10.2f} {len(observed_threads):>17}", flush=True)


def main():
    modes = ["sequential", "threads10", "threads100", "async10", "async100"]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["all"] + modes, default="all")
    parser.add_argument("--requests", type=int, default=100)
    parser.add_argument("--delay", type=float, default=0.2, help="Simulated API wait in seconds")
    args = parser.parse_args()
    if not 1 <= args.requests <= 1000 or not 0 <= args.delay <= 10:
        parser.error("Use 1..1000 requests and a delay of 0..10 seconds")

    context = multiprocessing.get_context("spawn")
    receiver, sender = context.Pipe(duplex=False)
    server = context.Process(target=serve_api, args=(sender, args.delay))
    server.start()
    sender.close()
    try:
        if not receiver.poll(15):
            raise RuntimeError("The local API did not start within 15 seconds")
        port = receiver.recv()
        base_url = f"http://127.0.0.1:{port}"
        print(f"API: {base_url}/products/1 (separate server PID {server.pid})")
        print(f"{args.requests} HTTP requests per mode; {args.delay}s API wait per request.")
        print("Request threads = distinct client threads executing request tasks, not total OS threads.")
        print(f"{'Mode':<14} {'Responses':>9} {'Seconds':>10} {'Request threads':>17}")
        for mode in modes if args.mode == "all" else [args.mode]:
            compare(base_url, args.requests, mode)
        print("All responses verified. Local API stopping.")
    finally:
        receiver.close()
        if server.is_alive():
            server.terminate()
        server.join(timeout=5)
        server.close()


if __name__ == "__main__":
    main()

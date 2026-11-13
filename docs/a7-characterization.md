# A7 characterization matrix

Production behavior is unchanged in this step. Existing work at e7257dd28 and
056ab0d74 is reused rather than duplicated.

| Component | Normal | Boundary | Failure/error |
| --- | --- | --- | --- |
| Import authorization | Owner can view status and retry an item | Missing job raises Http404; GET retry returns 405 without scheduling | Five existing cross-user tests deny viewing or mutation; task mocks verify no side effects |
| Login | Valid username/email authenticates; 2FA and forced-reset redirects remain | Five failures accepted; sixth blocked; five-minute expiry; separate IPs | Invalid password returns form error; even a correct password is blocked after limit; forwarded header cannot bypass |
| RedisStore | Ranked inserts and trims queued for each store | Empty stores queue no writes; deferred execution returns pipeline | redis.exceptions.ConnectionError propagates |

The existing trim-command mock describes current implementation, not correctness
of Redis rank arithmetic. A separate state-based regression test will investigate
that behavior during RED. No production behavior is changed here.

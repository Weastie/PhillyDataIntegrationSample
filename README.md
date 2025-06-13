# Data Integration Systems Engineer Final Evaluation

## Approach

When approaching a data integration task, there are many decisions to make, each of which may affect performance, validity, readability. and standardization of your process.

First, I had to choose a language. I chose Python because I am familiar with it, CityGeo uses it, and it is common for statistical work.

Next, I decided whether or not I would retrieve the data using APIs, or a CSV / other pre-downloaded format. In many ways, using pre-downloaded data can be beneficial, as
you only need to download the data one time, not each time you run the script. However, I ultimately decided to use APIs because they are always live with
current data, and they're more flexible in the event that additional directions or instructions come through. It does sacrifice speed, because APIs incur latency with each request.

Analyzing the first prompt is straight forward, with little room for ambiguity. The second and third prompt, however, require a bit of creativity.

The second prompt asks for what percentage of service requests resulted in the issuance of a code violation. Looking at the fields available in the violations database, there is no direct
entry that links a violation to the service request that instigated the violation. Insider knowledge of the Licenses & Inspections agency may provide insight as towards how they open cases,
but I did not have access to that knowledge. My best guess was to look for violations at the same address (matched by opa_account_num using the AIS API) that were opened within one month of
the service request being opened. An example of insider knowledge that could refine this link, would be if the Licenses & Inspections team had to respond to each service request within X days,
which would be more specific than one month. Even then, there's not necessarily an assurance that that violation was a direct result of the service request, so a proper analysis should include
a disclaimer.

The third prompt asks about what percentage of those service requests that resulted in a code violation have been closed. There could be multiple interpretations of this as well. For example, we could
look at whether, in the service requests database, the `status` is set to "Closed". However, the prompt specifies "(i.e. L&I has not finished inspecting them)", which might indicate that instead
we should look at the violations associated with the service request, and see if its `casestatus` is set to "CLOSED", which might more accurately represent whether L%I considers the case closed.
This also runs into another problem, where we may find multiple violations within one month of a service request at the same address. Insider knowledge of L&I could inform about whether all
those violations could be from the same service request, or if they might have separated sources. For my approach, I decided to only determine a service request as closed if all violations opened
within one month of it are closed.

### Sub-note: Performance

For my approach, I used synchronous API requests, meaning there will only ever be one request being made at a time. In past projects, I have used asychronous requests to make multiple
API requests simultaneously, but it has the potential to overwhelm the database or web server. I decided to err on the side of caution, and take a performance sacrifice. Learning the
standards and procedures of the CityGeo team would help me balance performance with modesty.

The script took 55 minutes and 11 seconds to run.

## Analysis
Since the beginning of 2025, 18701 out of 226410 service requests were associated with Licenses & Inspections.

Since the beginning of 2025, 5383 out of 18701, or 28.78% of service requests resulted in the issuance of a code violation.

Since the beginning of 2025, 1384 of the 5383, or 25.71% of violations from service requests were marked as closed.

## Final Notes
I've done similar work to this, using multiple APIs and joining data together, but only ever in informal situations, or in situations where performance is not critical. I lack knowledge of best
practices in this field, and I would be happy to learn about the tools, libraries, and standards used by the team to improve my methods. I'm a quick learner, and I especially learn quick when
I can read and analyze working examples of code, and adapt my style to match it.

About atomic git commits - In my current team, we use trunk based development. We basically use the description of a merge request as the description of the changes, rather than commit messages.
We had a relatively informal process, so I may need a bit more practice with writing detailed git commits.

I am well aware that my script is quite slow, and that I may have interpreted parts of the prompt incorrectly. I hope that my writing here shows that I at least understand the bigger picture, and with
minimal training could adapt my knowledge to design proper scripts.

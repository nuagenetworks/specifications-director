@import <RESTCappuccino/NURESTModelController.j>
@import "RESTFetchers/SDRESTFetchers.j"
@import "Jobs/SDJobs.j"

@import "SDAbstract.j"
@import "SDAPIInfo.j"
@import "SDAttribute.j"
@import "SDAuth.j"
@import "SDChildAPI.j"
@import "SDRepository.j"
@import "SDSpecification.j"

[[NURESTModelController defaultController] registerModelClass:SDAbstract];
[[NURESTModelController defaultController] registerModelClass:SDAPIInfo];
[[NURESTModelController defaultController] registerModelClass:SDAttribute];
[[NURESTModelController defaultController] registerModelClass:SDAuth];
[[NURESTModelController defaultController] registerModelClass:SDChildAPI];
[[NURESTModelController defaultController] registerModelClass:SDRepository];
[[NURESTModelController defaultController] registerModelClass:SDSpecification];

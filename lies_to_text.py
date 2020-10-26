from the_lies import lies as lies_dikt
from lie_fetcher import concat

lies_list = concat([lies for lies in lies_dikt.values()])
print("\n".join(lies_list))
